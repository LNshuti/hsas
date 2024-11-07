import os
import sqlite3
import pandas as pd

CSV_FILE_PATH = 'data/Hospital_Service_Area_2022.csv'
DB_FILE_PATH = 'databases/hsas.db'
TABLE_NAME = 'hsa_data'
PARQUET_FILE_PATH = 'data/processed/hsas.parquet'

def load_csv_to_sqlite_and_save_parquet(csv_file_path, db_file_path, table_name, parquet_file_path):
    """Loads a CSV file into a SQLite database, summarizes the data, handles missing values, and saves it as a Parquet file."""
    try:
        # Load CSV into DataFrame
        df = pd.read_csv(csv_file_path)
        print("Original DataFrame loaded:")
        print(df.head())

        print("\nDataFrame Info:")
        print(df.info())

        print("\nDataFrame Description:")
        print(df.describe(include='all'))

        print("\nMissing Values in Each Column:")
        print(df.isnull().sum())

        # Handle Specific Missing Value Representations
        # Columns where '*' should be replaced with 0
        columns_replace_star = ['TOTAL_DAYS_OF_CARE', 'TOTAL_CHARGES', 'TOTAL_CASES']
        
        for column in columns_replace_star:
            if column in df.columns:
                # Replace '*' with 0
                num_replacements = df[column].replace('*', 0).count() - df[column].replace('*', 0).count()
                df[column] = df[column].replace('*', 0)
                print(f"\nReplaced '*' with 0 in column '{column}'.")
                
                # Convert column to numeric (if not already)
                df[column] = pd.to_numeric(df[column], errors='coerce')
                print(f"Converted column '{column}' to numeric type.")
            else:
                print(f"\nWarning: Column '{column}' not found in DataFrame.")

        # Handle Missing Values
        # Strategy: Remove columns with all missing values and impute or remove rows with missing values in remaining columns
        # Step 1: Drop columns where all values are NaN
        initial_columns = df.shape[1]
        df.dropna(axis=1, how='all', inplace=True)
        dropped_columns = initial_columns - df.shape[1]
        if dropped_columns > 0:
            print(f"\nDropped {dropped_columns} columns with all missing values.")

        # Step 2: Identify remaining columns with missing values
        missing_values = df.isnull().sum()
        columns_with_missing = missing_values[missing_values > 0].index.tolist()
        
        if columns_with_missing:
            print(f"\nColumns with missing values: {columns_with_missing}")
            # Define columns that were processed to replace '*' with 0
            for column in columns_with_missing:
                if column in columns_replace_star:
                    # These columns have already had '*' replaced with 0 and converted to numeric
                    # Now, handle any remaining missing values by imputing with 0
                    df[column].fillna(0, inplace=True)
                    print(f"Imputed remaining missing values in column '{column}' with 0.")
                elif df[column].dtype in ['float64', 'int64']:
                    median_value = df[column].median()
                    df[column].fillna(median_value, inplace=True)
                    print(f"Imputed missing values in numerical column '{column}' with median: {median_value}.")
                else:
                    mode_value = df[column].mode()[0]
                    df[column].fillna(mode_value, inplace=True)
                    print(f"Imputed missing values in categorical column '{column}' with mode: {mode_value}.")
        else:
            print("\nNo missing values detected.")

        print("\nDataFrame after handling missing values:")
        print(df.head())

        print("\nSummary after handling missing values:")
        print(df.info())
        print(df.describe(include='all'))

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
        print("\nDataFrame with cleaned column names:")
        print(df.head())

        # Create SQLite database and insert data
        os.makedirs(os.path.dirname(db_file_path), exist_ok=True)
        with sqlite3.connect(db_file_path) as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"\nData successfully loaded into {db_file_path} in table '{table_name}'.")

        # Save DataFrame as Parquet file
        os.makedirs(os.path.dirname(parquet_file_path), exist_ok=True)
        df.to_parquet(parquet_file_path, index=False)
        print(f"Data successfully saved as Parquet file at {parquet_file_path}.")

    except Exception as e:
        print(f"Error loading CSV file into SQLite and saving as Parquet: {e}")

# Load CSV into SQLite and save as Parquet
load_csv_to_sqlite_and_save_parquet(CSV_FILE_PATH, DB_FILE_PATH, TABLE_NAME, PARQUET_FILE_PATH)