import sqlite3
import pandas as pd

CSV_FILE_PATH = 'backend/data/Hospital_Service_Area_2022.csv'
DB_FILE_PATH = 'backend/databases/hsas.db'
TABLE_NAME = 'hsa_data'

def load_csv_to_sqlite(csv_file_path, db_file_path, table_name):
    """Loads a CSV file into a SQLite database."""
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Clean column names
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace('.', '_').str.replace('/', '_').str.replace('-', '_').str.replace('#', '').str.replace('$', '')
        
        # Create SQLite database and insert data
        with sqlite3.connect(db_file_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data successfully loaded into {db_file_path} in table {table_name}.")
    except Exception as e:
        print(f"Error loading CSV file into SQLite: {e}")

# Load CSV into SQLite
load_csv_to_sqlite(CSV_FILE_PATH, DB_FILE_PATH, TABLE_NAME)