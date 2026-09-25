import psycopg
from app.config import POSTGRES_DB_URL

def get_connection():
    return psycopg.connect(POSTGRES_DB_URL)