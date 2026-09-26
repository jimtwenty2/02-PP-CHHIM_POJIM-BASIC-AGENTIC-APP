# BASIC AGENTIC APPLICATION


## Project Overview

This project is an **Agentic Library Management System** that uses an AI agent to interact with a library database through predefined tools.

The system uses **PostgreSQL** to manage books and borrowing records. The AI agent can call tools to search for books, check availability, and perform borrowing actions based on the user's permissions.

### Available Tools

* **`list_books()`** — Lists all books with their title, author, and available copies.
* **`search_book(query)`** — Searches for books by title.
* **`check_availability(book_id)`** — Checks the number of available copies for a book.
* **`borrow_book(book_id, quantity)`** — Borrows books and records each borrowing action in the `borrow_log` table.

### User Roles

The system has two main roles:

**Admin**

* Can use all available tools.
* Can list and search books.
* Can check book availability.
* Can borrow books.

**User**

* Can list books.
* Can search for books.
* Can check book availability.
* **Cannot borrow books.**

The permission system ensures that the agent can only perform actions that the current user is authorized to perform.


## Requirements and Installation

Before running the project, make sure you have:

* **Git**
* **Python**
* **uv**
* **Docker & Docker Compose**
* **Ollama**

The Ollama model you use **must support tool calling**, because the agent relies on LLM tool-calling capabilities.
Some supported models include:
- qwen3
- qwen2.5
- qwen2.5-coder
- llama3.1
- llama4
- mistral-nemo
- devstral
- gpt-oss

---

## 1. Clone the Repository

```bash
git clone https://github.com/jimtwenty2/02-PP-CHHIM_POJIM-BASIC-AGENTIC-APP.git
```

Enter the project directory:

```bash
cd 02-PP-CHHIM_POJIM-BASIC-AGENTIC-APP
```

---

## 2. Set Up Environment Variables

Create your own `.env` file from the provided example:

```bash
cp .env.example .env
```

Open `.env` and configure the required values for your environment.

For example:

```env
MODEL=<model_name>

OLLAMA_BASE_URL=http://localhost:11434/v1

# Postgres db config
POSTGRES_DB_PORT=<database_port>
POSTGRES_DB_NAME=<database_name>
POSTGRES_DB_USER=<database_user>
POSTGRES_DB_HOST=localhost
POSTGRES_DB_PASSWORD=<databse_secret>
```
---

## 3. Install Python Dependencies

This project uses **uv** for Python package and virtual environment management.

If you don't have `uv` installed, install it first.

Then sync the project dependencies:

```bash
uv sync
```

This will create the project's virtual environment and install the required dependencies.

---

## 4. Set Up Ollama

Make sure Ollama is installed and running:

```bash
ollama serve
```

In another terminal, pull a model that supports **tool calling**:

```bash
ollama pull <MODEL_NAME>
```

Check that the model is available:

```bash
ollama list
```

Then make sure the model name in your `.env` matches the model you pulled:

```env
MODEL=<MODEL_NAME>
```

> **Important:** The LLM must support **tool calling**. A model that does not support tool calling may not work correctly with the agent.

---

## 5. Start the Database

The project uses **Docker Compose** to run the PostgreSQL database.

Start the database services:

```bash
docker compose up -d
```

Check that the containers are running:

```bash
docker compose ps
```

You should see the PostgreSQL container running.

## 6. Initialize the Database

After the PostgreSQL database is running, initialize the database using:

```bash
uv run python -m app.init_db
```

This command prepares the database for the application.

### What does `app.init_db` do?

The initialization script:

1. Connects to the PostgreSQL database using the configuration in `.env`.
2. Creates the required database tables if they do not already exist.
3. Creates the following tables:

   * `books` — stores information about available books.
   * `borrow_log` — stores book borrowing records.
4. Inserts initial sample data into the `books` table.

The database structure will look like:

```text
PostgreSQL
│
├── books
│   └── Initial book data
│
└── borrow_log
    └── Borrowing records
```

Run the initialization command after starting PostgreSQL:

```bash
docker compose up -d

uv run python -m app.init_db
```

> **Note:** Run the initialization script only after the PostgreSQL container is running and your `.env` database configuration is correct.
