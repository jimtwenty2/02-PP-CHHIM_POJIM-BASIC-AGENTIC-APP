import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_DB_HOST", "localhost"),
        port=os.getenv("POSTGRES_DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB_NAME"),
        user=os.getenv("POSTGRES_DB_USER"),
        password=os.getenv("POSTGRES_DB_PASSWORD"),
    )