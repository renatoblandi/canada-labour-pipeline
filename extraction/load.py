import os
import psycopg
from dotenv import load_dotenv

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

if __name__ == "__main__":
    with get_connection() as conn:
        create_bronze_schema(conn)
        create_bronze_table(conn)