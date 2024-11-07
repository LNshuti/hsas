import os
import sqlite3
import pandas as pd

CSV_FILE_PATH = 'data/Hospital_Service_Area_2022.csv'
DB_FILE_PATH = 'databases/hsas.db'
TABLE_NAME = 'hsa_data'
PARQUET_FILE_PATH = 'data/processed/hsas.parquet'

def load_csv_to_sqlite_and_save_parquet(csv_file_path, db_file_path, table_name, parquet_file_path):
    """Loads a CSV file into a SQLite database and saves it as a Parquet file."""
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(csv_file_path)
        print("Original DataFrame loaded:")
        print(df.head())

        # Clean column names
        df.columns = (
            df.columns
            .str.lower()
            .str.replace(' ', '_', regex=False)
            .str.replace('.', '_', regex=False)
            .str.replace('/', '_', regex=False)
            .str.replace('-', '_', regex=False)
            .str.replace('#', '', regex=False)
            .str.replace('$', '', regex=False)
        )
        print("DataFrame with cleaned column names:")
        print(df.head())

        # Create SQLite database and insert data
        os.makedirs(os.path.dirname(db_file_path), exist_ok=True)
        with sqlite3.connect(db_file_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data successfully loaded into {db_file_path} in table '{table_name}'.")

        # Save DataFrame as Parquet file
        os.makedirs(os.path.dirname(parquet_file_path), exist_ok=True)
        df.to_parquet(parquet_file_path, index=False)
        print(f"Data successfully saved as Parquet file at {parquet_file_path}.")

    except Exception as e:
        print(f"Error loading CSV file into SQLite and saving as Parquet: {e}")

# Load CSV into SQLite and save as Parquet
load_csv_to_sqlite_and_save_parquet(CSV_FILE_PATH, DB_FILE_PATH, TABLE_NAME, PARQUET_FILE_PATH)