import logging
import gradio as gr
import pandas as pd
import plotly.express as px
import folium
import numpy as np
import geopandas as gpd
from folium.plugins import MarkerCluster
from sklearn.neighbors import BallTree
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import math
import os

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load datasets
df_md_final1 = pd.read_csv("backend/data/location-of-auto-businesses.csv")
cbg_geographic_data = pd.read_csv("backend/data/cbg_geographic_data.csv")

# Create DataFrames for the 2020 and 2010 populations
population_2020_data = {
    'County': ['Shelby', 'Davidson', 'Knox', 'Hamilton', 'Rutherford', 'Williamson', 'Montgomery', 'Sumner', 'Blount', 'Washington', 
               'Madison', 'Sevier', 'Maury', 'Wilson', 'Bradley'],
    'Population_2020': [929744, 715884, 478971, 366207, 341486, 247726, 220069, 196281, 135280, 133001, 
                        98823, 98380, 100974, 147737, 108620]
}
df_population_2020 = pd.DataFrame(population_2020_data)

df_population_2010 = cbg_geographic_data.groupby('cntyname')['pop10'].sum().reset_index().sort_values(by='pop10', ascending=False)
df_population_2010.rename(columns={'cntyname': 'County', 'pop10': 'Population_2010'}, inplace=True)

# Merge the 2010 and 2020 population data for side-by-side comparison
df_population_comparison = pd.merge(df_population_2010, df_population_2020, on='County')

# Define Business Types
df_md_final1['business_type'] = np.where(df_md_final1['name'].str.contains("Autozone", case=False, na=False), "Autozone", 
    np.where(df_md_final1['name'].str.contains("Napa Auto Parts", case=False, na=False), "Napa Auto", 
        np.where(df_md_final1['name'].str.contains("Firestone Complete Auto Care", case=False, na=False), "Firestone",                                 
            np.where(df_md_final1['name'].str.contains("O'Reilly Auto Parts", case=False, na=False), "O'Reilly Auto",
                np.where(df_md_final1['name'].str.contains("Advance Auto Parts", case=False, na=False), "Advance Auto",
                    np.where(df_md_final1['name'].str.contains("Toyota|Honda|Kia|Nissan|Chevy|Ford|Carmax|GMC", case=False, na=False), 
                             "Car Dealership", 
                             "Other Auto Repair Shops")
                )
            )
        )
    )
)

# Load the County shapefile
county_shapefile_path = "backend/data/county/01_county-shape-file.shp"
if not os.path.exists(county_shapefile_path):
    raise FileNotFoundError(f"County shapefile not found at {county_shapefile_path}. Please ensure the file exists.")
    
counties_geo = gpd.read_file(county_shapefile_path)
counties_geo = counties_geo[counties_geo['statefp'] == '47']  # Tennessee FIPS code

# Load the HSA shapefile
hsa_shapefile_path = "backend/data/hsa/01_hsa-shape-file.shp"
if not os.path.exists(hsa_shapefile_path):
    raise FileNotFoundError(f"HSA shapefile not found at {hsa_shapefile_path}. Please ensure the file exists.")
    
hsa_geo = gpd.read_file(hsa_shapefile_path)
if 'hsastate' in hsa_geo.columns:
    hsa_geo = hsa_geo[hsa_geo['hsastate'].isin(['TN'])]
elif 'STATEFP' in hsa_geo.columns:
    hsa_geo = hsa_geo[hsa_geo['STATEFP'].isin(['47'])]
else:
    raise KeyError("Column to filter state in HSA shapefile not found.")

# Load the HRR shapefile
hrr_shapefile_path = "backend/data/hrr/01_hrr-shape-file.shp"
if not os.path.exists(hrr_shapefile_path):
    raise FileNotFoundError(f"HRR shapefile not found at {hrr_shapefile_path}. Please ensure the file exists.")
    
hrr_geo = gpd.read_file(hrr_shapefile_path)
if 'hrrstate' in hrr_geo.columns:
    hrr_geo = hrr_geo[hrr_geo['hrrstate'].isin(['TN'])]
elif 'STATEFP' in hrr_geo.columns:
    hrr_geo = hrr_geo[hrr_geo['STATEFP'].isin(['47'])]
else:
    raise KeyError("Column to filter state in HRR shapefile not found.")

# Function to create a Folium map with selected geographical boundaries and markers
def create_map(geo_layer="Counties", business_filters=["All"]):
    logger.info(f"Creating map with geo_layer: {geo_layer} and business_filters: {business_filters}")
    
    m = folium.Map(location=[35.8601, -86.6602], zoom_start=7)
    
    try:
        # Select the appropriate GeoDataFrame based on geo_layer
        if geo_layer == "Counties":
            geo_data = counties_geo
        elif geo_layer == "HSAs":
            geo_data = hsa_geo
        elif geo_layer == "HRRs":
            geo_data = hrr_geo
        else:
            geo_data = counties_geo  # Default to counties
        logger.info(f"Geo layer {geo_layer} selected.")
        
        # Add selected geographical boundaries
        folium.GeoJson(geo_data, name=geo_layer).add_to(m)
    except Exception as e:
        logger.error(f"Error loading GeoData for {geo_layer}: {e}")
    
    # Initialize Marker Cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    # Filter based on Business 
    if "All" not in business_filters:
        filtered_df = df_md_final1[df_md_final1['business_type'].isin(business_filters)]
    else:
        filtered_df = df_md_final1.copy()
    
    logger.info(f"Filtered {len(filtered_df)} businesses based on filters: {business_filters}")

    # Add markers to the map
    for _, row in filtered_df.iterrows():
        folium.Marker(
            location=[row['md_y'], row['md_x']],
            popup=f"<b>{row['name']}</b><br>{row.get('address', 'N/A')}, {row.get('city', 'N/A')}, TN {row.get('postal_code', 'N/A')}",
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)
    
    folium.LayerControl().add_to(m)
    
    logger.info("Map creation completed.")
    return m._repr_html_()

# Function to create the bar plot for 2020 Tennessee population (top 15 counties)
def plot_2020_population_top15():
    fig = px.bar(df_population_2020, 
                 x='County', 
                 y='Population_2020', 
                 title='Tennessee Population 2020', 
                 labels={'County': 'County', 'Population_2020': 'Population'},
                 color='Population_2020',
                 color_continuous_scale='Blues')
    
    fig.update_layout(xaxis={'categoryorder':'total descending'}, template='plotly_white')
    return fig

# Function to create a side-by-side bar chart for the 2010 and 2020 Tennessee population by county
def plot_population_comparison():
    df_melted = df_population_comparison.melt(id_vars='County', value_vars=['Population_2010', 'Population_2020'],
                                              var_name='Year', value_name='Population')
    fig = px.bar(df_melted, 
                 x='County', 
                 y='Population', 
                 color='Year', 
                 barmode='group', 
                 title="Tennessee Population Comparison: 2010 vs 2020", 
                 labels={'County': 'County', 'Population': 'Population'},
                 color_discrete_map={'Population_2010': 'lightgreen', 'Population_2020': 'lightblue'})
    
    fig.update_layout(xaxis={'categoryorder': 'total descending'}, template='plotly_white')
    return fig

# Nearest Neighbor Search Setup
# Prepare the data for nearest neighbor search
def prepare_nearest_neighbor():
    # Convert coordinates to radians for BallTree
    coords = df_md_final1[['md_y', 'md_x']].to_numpy()
    radians_coords = np.radians(coords)
    tree = BallTree(radians_coords, metric='haversine')
    return tree, radians_coords

tree, radians_coords = prepare_nearest_neighbor()

# Geocoder setup
geolocator = Nominatim(user_agent="tn_auto_shops_app")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Gradio Interface
with gr.Blocks(theme=gr.themes.Default()) as app:
    gr.Markdown("# 🚗 Tennessee Auto Repair Businesses Dashboard")
    
    with gr.Tab("Overview"):
        gr.Markdown("## 📊 Tennessee Population Statistics")
        
        with gr.Row():
            
            with gr.Column():
                gr.Markdown("### 2010 vs 2020 Population Comparison")
                pop_comp = gr.Plot(plot_population_comparison)
        
        gr.Markdown("### 🛠️ Auto Businesses in Tennessee")
        manual_table = gr.Dataframe(
            headers=["Location Name", "Street Address", "City", "State", "Postal Code"],
            datatype=["str", "str", "str", "str", "str"],
            value=[
                ["AutoZone", "257 Wears Valley Rd", "Pigeon Forge", "Tennessee", "37863"],
                ["Sterling Auto", "2064 Wilma Rudolph Blvd", "Clarksville", "Tennessee", "37040"],
                ["Advance Auto Parts", "2124 N Highland Ave", "Jackson", "Tennessee", "38305"],
                # ... (Add other rows as needed)
            ],
            row_count=10,
            interactive=False
        )
    
        gr.Markdown("### 📍 Interactive Map")
        map_output_overview = gr.HTML(create_map(geo_layer="Counties", business_filters=["All"]))
        
    with gr.Tab("📍 Shops in TN HSAs"):
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### Filter Shops by Business Type")
                business_options_hsa = ["All"] + sorted(df_md_final1['business_type'].unique())
                business_filter_hsa = gr.CheckboxGroup(label="Select Business ", choices=business_options_hsa, value=["All"])
                reset_button_hsa = gr.Button("Reset Filters")
            with gr.Column(scale=4):
                shops_hsa_map = gr.HTML()
        
        def update_hsa_map(business_filters):
            if "All" in business_filters or not business_filters:
                business_filters = ["All"]
            return create_map(geo_layer="HSAs", business_filters=business_filters)
        
        business_filter_hsa.change(fn=update_hsa_map, inputs=[business_filter_hsa], outputs=[shops_hsa_map])
        reset_button_hsa.click(fn=lambda: (["All"], create_map(geo_layer="HSAs", business_filters=["All"])),
                               inputs=None, outputs=[business_filter_hsa, shops_hsa_map])
        
    
    with gr.Tab("🔍 Help"):
        gr.Markdown("""
        ## How to Use This Dashboard
        
        - **Overview Tab:** Provides population statistics and a summary map of all auto businesses in Tennessee.
        
        - **Shops in TN Counties/HSAs/HRRs Tabs:**
            - **Filter by Business Type:** Use the checkboxes to select one or multiple business types to display on the map.
            - **Filter by Geographical Area:** Depending on the tab, you can filter businesses based on Counties, HSAs, or HRRs.
            - **Reset Filters:** Click the reset button to clear all selected filters and view all businesses.
            - **Interactive Map:** Zoom in/out, click on markers to view business details, and use the search bar to find specific businesses.
        
        - **Nearest Shop Finder Tab:**
            - **Enter Address:** Type your address in the textbox. As you type, address suggestions will appear. Select one or press Enter to find the nearest auto shop.
            - **View Results:** The map will display your location and the nearest auto shop with a line connecting them.
        
        """)
    
    gr.Markdown("### 📄 Source: Yellow Pages")

app.launch(server_name="0.0.0.0", server_port=7860, share=True)
