import gradio as gr
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import requests
from io import StringIO

def load_intox_data():
    """
    Load and clean intoxication data from a CSV URL.
    """
    url = "https://raw.githubusercontent.com/walkerke/geog30323/refs/heads/master/intoxication.csv"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError("Failed to fetch intoxication data.")
    
    # Read CSV into DataFrame
    intox_df = pd.read_csv(StringIO(response.text))
    
    # Clean column names
    intox_df.columns = [col.strip().lower().replace(" ", "_") for col in intox_df.columns]
    
    # Drop rows with missing values
    intox_df = intox_df.dropna(subset=["longitude", "latitude"])
    
    return intox_df

def load_tn_boundaries():
    """
    Load Tennessee boundaries using geopandas.
    """
    # Using Natural Earth low-resolution data for US states
    usa = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    tn = usa[usa.name == "Tennessee"]
    
    if tn.empty:
        raise ValueError("Failed to load Tennessee boundaries.")
    
    return tn

def create_map(intox_df, tn_gdf):
    """
    Create an interactive map using pydeck.
    """
    # Define the initial view state centered on Tennessee
    view_state = pdk.ViewState(
        longitude=-86.6923,
        latitude=35.5175,
        zoom=7,
        pitch=0
    )
    
    # Layer for Tennessee boundaries
    tn_layer = pdk.Layer(
        "GeoJsonLayer",
        tn_gdf.__geo_interface__,
        stroked=True,
        filled=True,
        fill_color=[173, 216, 230, 50],  # Light blue with transparency
        line_color=[0, 0, 255],
        line_width=2,
        pickable=False
    )
    
    # Scatterplot layer for intoxication points
    intox_layer = pdk.Layer(
        "ScatterplotLayer",
        intox_df,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=1,
        radius_max_pixels=10,
        line_width_min_pixels=1,
        get_position='[longitude, latitude]',
        get_fill_color='[255, 0, 0, 160]',  # Red with some transparency
        get_line_color='[255, 255, 255]',
        line_width=1
    )
    
    # Heatmap layer for intoxication density
    heatmap_layer = pdk.Layer(
        "HeatmapLayer",
        intox_df,
        get_position='[longitude, latitude]',
        auto_highlight=True,
        radius=10,
        intensity=1,
        threshold=0.05,
        aggregation='SUM',
        get_weight='1',
        color_range=[
            [0, 0, 255, 0],
            [0, 0, 255, 255],
            [0, 255, 255, 255],
            [0, 255, 0, 255],
            [255, 255, 0, 255],
            [255, 0, 0, 255]
        ]
    )
    
    # Combine layers
    layers = [tn_layer, intox_layer, heatmap_layer]
    
    # Create the deck.gl map
    r = pdk.Deck(
        map_style='mapbox://styles/mapbox/open-street-map',
        initial_view_state=view_state,
        layers=layers,
        tooltip={"text": "Intoxication Incident"}
    )
    
    return r.to_html()

def generate_map():
    """
    Load data, create map, and return HTML.
    """
    intox_df = load_intox_data()
    tn_gdf = load_tn_boundaries()
    map_html = create_map(intox_df, tn_gdf)
    return map_html

# Define Gradio Interface
iface = gr.Interface(
    fn=generate_map,
    inputs=[],
    outputs=gr.HTML(label="Tennessee Intoxication Map"),
    title="Tennessee Intoxication Incidents Map",
    description="Interactive map showing intoxication incidents in Tennessee with heatmap overlay."
)

# Launch the Gradio app
if __name__ == "__main__":
    iface.launch()