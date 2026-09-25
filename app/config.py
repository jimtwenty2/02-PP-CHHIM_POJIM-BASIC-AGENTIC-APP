import os
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("POSTGRES_DB_HOST", "localhost")
port = os.getenv("POSTGRES_DB_PORT", "5432")
dbname = os.getenv("POSTGRES_DB_NAME")
username = os.getenv("POSTGRES_DB_USER")
password = os.getenv("POSTGRES_DB_PASSWORD")

POSTGRES_DB_URL = f'postgresql://{username}:{password}@{host}:{port}/{dbname}'

MAX_ITERATIONS = 6
MAX_TOOL_CALLS = 5

SYSTEM_PROMPT = (
    "You are a helpful library assistant. "
    "Use the available tools to list books, search books, check availability, and borrow books. "
    "Only use a tool when the user asks about books. "
    "Book ids are numbers that come from tool results, so never guess them. "
    "Answer only from tool results. "
    "If a tool returns an error, tell the user clearly."
)

VALID_ROLES = ("customer", "admin")