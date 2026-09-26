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

## Safety Controls

This project includes basic safety controls to make the AI agent more secure and predictable.

### 1. Basic Input Validation

The project uses **Pydantic** to validate tool inputs before executing them. This helps ensure values such as book IDs and quantities are valid.

```python
try:
    clean = schema(**args)
except ValidationError:
    return {"ok": False, "error": "INVALID_INPUT"}
```

### 2. Basic Error Handling

Tool execution is wrapped with error handling. If an unexpected error occurs, the application returns a controlled error instead of exposing the internal exception.

```python
try:
    return function(**clean.model_dump())
except Exception:
    return {"ok": False, "error": "TOOL_FAILED"}
```

### 3. Tool Allowlist

Only tools registered in `TOOL_REGISTRY` can be executed. This prevents the agent from calling arbitrary functions.

```python
if name not in TOOL_REGISTRY:
    return {"ok": False, "error": "TOOL_NOT_ALLOWED"}
```

### 4. Role-Based Permissions

The project has two roles: `customer` and `admin`.

Customers can view and search books and check availability, while admins have access to all available tools, including borrowing books.

```python
PERMISSIONS = {
    "customer": {
        "list_books",
        "search_book",
        "check_availability",
    },
    "admin": {
        "list_books",
        "search_book",
        "check_availability",
        "borrow_book",
    },
}
```

The user's role is checked before a tool is executed:

```python
if name not in PERMISSIONS.get(user_role, set()):
    return {"ok": False, "error": "PERMISSION_DENIED"}
```

### 5. Agent Loop

The agent follows a simple **Decision → Action → Observation** loop:

```text
User Request
     ↓
  Decision
  (LLM)
     ↓
  Action
 (Tool Call)
     ↓
 Observation
 (Tool Result)
     ↓
  Decision
     ↓
Final Answer
```

* **Decision:** The LLM decides whether a tool is needed.
* **Action:** The selected tool is executed through `run_tool()`.
* **Observation:** The tool result is returned to the LLM.
* The loop continues until the LLM provides a final answer or reaches the configured limits.

```python
for iteration in range(1, MAX_ITERATIONS + 1):
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
    )
```

The agent is limited by:

```python
MAX_ITERATIONS = 6
MAX_TOOL_CALLS = 5
```

These limits help prevent endless agent loops and excessive tool calls.


### 6. Controlled Tool Errors

Library tools return controlled errors for expected situations, such as a book not being found or having no available copies.

```python
if not row:
    return {"ok": False, "error": "BOOK_NOT_FOUND"}

return {"ok": False, "error": "OUT_OF_STOCK"}
```

These controls ensure that the agent can only use approved tools, validates inputs, respects user permissions, handles errors safely, and stops after reaching execution limits.


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

### 1. Clone the Repository

```bash
git clone https://github.com/jimtwenty2/02-PP-CHHIM_POJIM-BASIC-AGENTIC-APP.git
```

Enter the project directory:

```bash
cd 02-PP-CHHIM_POJIM-BASIC-AGENTIC-APP
```

---

### 2. Set Up Environment Variables

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

### 3. Install Python Dependencies

This project uses **uv** for Python package and virtual environment management.

If you don't have `uv` installed, install it first.

Then sync the project dependencies:

```bash
uv sync
```

This will create the project's virtual environment and install the required dependencies.

---
### 4. Set Up Ollama

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

### 5. Start the Database

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

### 6. Initialize the Database

After the PostgreSQL database is running, initialize the database using:

```bash
uv run python -m app.init_db
```

This command prepares the database for the application.

#### What does `app.init_db` do?

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

### 7. Check Database

After init database, You can view the PostgreSQL tables and their data inside the Docker container:

```bash
docker compose exec db psql -U <POSTGRES_DB_USER> -d <POSTGRES_DB_NAME>
```

Inside PostgreSQL:

```sql
-- List tables
\dt

-- View books table structure
\d books

-- View books data
SELECT * FROM books;

-- View borrowing records
SELECT * FROM borrow_log;
```

Exit PostgreSQL with:

```sql
\q
```
### 8. Run the Application

Start the application from the project root directory:

```bash
uv run python main.py
```

The application will ask you to choose a role:

```text
Role (customer/admin):
```

Available roles:

* `customer`
* `admin`

Enter your library request and the AI agent will process it using the available tools and the permissions of the selected role.

To exit the application:

```text
quit
```

## Test cases
### Case 1 - List Books | Role : Customer
```text
Query: Show me all books
```
![case 1](./screenshots/Screenshot%20From%202026-09-26%2013-17-49.png)

### Case 2 - Search Book and its copies | Role: Customer
```text
Query: Search for Kolab Pailin and tell me how many copies are available.
```
In this case, The agent can use multiple tools in sequence when one tool does not provide all the required information.
```text
┌─────────────────────────────┐
│        User Request         │
│ "Find Kolab Pailin copies"  │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│ search_book("Kolab Pailin") │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│        Book ID = 2          │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│   check_availability(2)     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│     10 copies available     │
└──────────────┬──────────────┘
               ↓
┌─────────────────────────────┐
│       Final Answer          │
└─────────────────────────────┘
```
![case 2](./screenshots/Screenshot%20From%202026-09-26%2013-28-09.png)

### Case 3 — Customer Attempts to Borrow | Role: Customer
```text
Query: Borrow 1 copy of book id 2 
```
The customer requested to borrow 1 copy of book ID 2. The agent selected the borrow_book tool, but the permission layer checked the user's role and rejected the request because customers are not allowed to borrow books.

The tool returned PERMISSION_DENIED, and the agent informed the customer that admin privileges are required.
![case 3](./screenshots/Screenshot%20From%202026-09-26%2013-35-41.png)

### Case 4 — Invalid Input Test | Role: Admin
```text
Query: Borrow 1 copy of book id -1 
```
The agent attempted to call borrow_book, but the input validation rejected book_id = -1 because a valid book ID must be a positive integer. The tool returned INVALID_INPUT, and the agent informed the user to provide a valid book ID.
![case 4](./screenshots/Screenshot%20From%202026-09-26%2013-42-50.png)

### Case 5 — Admin Borrows 2 Book | Role: Admin
```text
Query: Borrow 2 copy of book id 1 
```
The admin requested to borrow 2 copies of book ID 1. The agent called the borrow_book tool with the correct book_id and quantity. The request passed permission and input validation, successfully updated the database, and recorded the borrowing. The result shows that 2 copies were borrowed and 27 copies remain.
![case 5](./screenshots/Screenshot%20From%202026-09-26%2013-59-17.png)

