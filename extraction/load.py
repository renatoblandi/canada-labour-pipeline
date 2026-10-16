import os
import psycopg
import zipfile
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# connect to db
def get_connection():
    conn = psycopg.connect(
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"]
    )
    return conn

# create bronze schema
def create_bronze_schema(conn):
    query = """
        CREATE SCHEMA IF NOT EXISTS bronze;
    """
    conn.execute(query)

# create bronze table (everything as TEXT)
def create_bronze_table(conn):
    query = """
        CREATE TABLE IF NOT EXISTS bronze.labour_force (
            ref_date TEXT,
            geo TEXT,
            dguid TEXT,
            labour_force_characteristics TEXT,
            gender TEXT,
            age_group TEXT,
            statistics TEXT,
            data_type TEXT,
            uom TEXT,
            uom_id TEXT,
            scalar_factor TEXT,
            scalar_id TEXT,
            vector TEXT,
            coordinate TEXT,
            value TEXT,
            status TEXT,
            symbol TEXT,
            terminated TEXT,
            decimals TEXT,
            loaded_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
    """
    conn.execute(query)

def load_bronze(conn, zip_path):
    # delete all rows on table
    query = """
        TRUNCATE bronze.labour_force;
    """
    conn.execute(query)

    query = """
        COPY bronze.labour_force (
            ref_date,
            geo,
            dguid,
            labour_force_characteristics,
            gender,
            age_group,
            statistics,
            data_type,
            uom,
            uom_id,
            scalar_factor,
            scalar_id,
            vector,
            coordinate,
            value,
            status,
            symbol,
            terminated,
            decimals
        )
        FROM STDIN
        WITH (FORMAT csv, HEADER true)
    """
    
    with conn.cursor() as cur:
        with cur.copy(query) as copy:
            with zipfile.ZipFile(zip_path) as z:
                with z.open("14100287.csv") as f:
                    while chunk := f.read(1024 * 1024):
                        copy.write(chunk)

def run_bronze_load(zip_path):
    with get_connection() as conn:
        create_bronze_schema(conn)
        create_bronze_table(conn)
        load_bronze(conn, zip_path)

if __name__ == "__main__":
    run_bronze_load(Path("data/raw/14100287-eng.zip"))