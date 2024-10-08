import os
import sqlite3
import asyncio
import modal

# Define the Modal App
app = modal.App("hsas-datasette")

# Define the image to be used, including the necessary packages for Datasette
datasette_image = (
    modal.Image.debian_slim()
    .pip_install("datasette~=0.63.2", "sqlite-utils")
)

# Define the persistent volume where the database is stored
VOLUME_DIR = "/cache-vol"
DB_PATH = f"{VOLUME_DIR}/backend/databases/hsas.db"

# Mount the volume for database access
volume = modal.Volume.from_name("hsas-datasette-cache-vol")

# Function to initialize the SQLite database if it does not exist
def initialize_database(db_path):
    if not os.path.exists(db_path):
        print(f"Database file {db_path} not found. Initializing new database.")
        conn = sqlite3.connect(db_path)  # Create the db file
        # Run schema creation SQL here (if needed)
        conn.execute('''CREATE TABLE IF NOT EXISTS example_table (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL);''')
        conn.commit()
        conn.close()
    else:
        print(f"Database file {db_path} exists.")


# Serve the `hsas.db` SQLite database using Datasette
@app.function(
    image=datasette_image,
    volumes={VOLUME_DIR: volume},
    allow_concurrent_inputs=16,
)
@modal.asgi_app()
def ui():
    from datasette.app import Datasette
    
    # Ensure the database is initialized or fallback to in-memory if not
    initialize_database(DB_PATH)

    # Instantiate the Datasette instance with the `hsas.db` database
    ds = Datasette(files=[DB_PATH], settings={"sql_time_limit_ms": 10000})
    asyncio.run(ds.invoke_startup())
    return ds.app()

# Entrypoint for running the app locally
@app.local_entrypoint()
def run():
    print("Deploying hsas.db database with Datasette...")
    initialize_database(DB_PATH)
