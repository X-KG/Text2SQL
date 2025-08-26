# 🧠 TEXT2SQL - Sakila

A simple FastAPI-based application that takes natural language queries and converts them into valid SQL SELECT statements using the ChatGPT API, then runs the query on the *Sakila* MySQL database and returns the result.

---

## 🚀 Features

- Converts natural language input to SQL queries
- Uses sqlglot to validate and restrict to SELECT-only statements
- Executes against the customer table of the Sakila sample database
- Limits output using max_rows parameter
- Built with: *FastAPI, **OpenAI, **sqlglot, **MySQL*

---

## 🧱 Schema Info

This demo is hardcoded to work with the customer table from the [Sakila sample MySQL database](https://dev.mysql.com/doc/sakila/en/).

Schema passed to the LLM looks like:


Table: customer
Columns: customer_id, store_id, first_name, last_name, email, address_id, active, create_date, last_update


To use your own schema:
- Replace the hardcoded schema string in core/llm.py
- Keep the format: "Table: <table_name>\nColumns: col1, col2, col3, ..."
- Make sure the MySQL DB also has the matching schema

You can also dynamically fetch schema later using INFORMATION_SCHEMA.COLUMNS, but this app uses a static version for now.

---

## 🛠️ Local Setup

### 1. Clone the repo

bash
git clone https://github.com/your-username/text2sql-sakila.git
cd text2sql-sakila


### 2. Create virtual environment

bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate


### 3. Install dependencies

bash
uv pip install -r requirements.txt


If you're using [uv](https://github.com/astral-sh/uv):

bash
uv venv
uv pip install -r requirements.txt


### 4. Create .env file

env
OPENAI_API_KEY=your-api-key
MYSQL_URL=mysql+mysqlconnector://user:password@localhost:3306/sakila


(You can copy from .env.example)

---

## ▶️ Run the API

bash
uvicorn app.main:app --reload


Visit the docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Example Input / Output

### Request

json
POST /api/query

{
  "nl_query": "Give me first names of all active customers",
  "max_rows": 10
}


### Response

json
{
  "sql_query": "SELECT first_name FROM customer WHERE active = 1;",
  "rows": [
    { "first_name": "MARY" },
    { "first_name": "PATRICIA" },
    { "first_name": "LINDA" },
    { "first_name": "BARBARA" },
    { "first_name": "ELIZABETH" },
    { "first_name": "JENNIFER" }
  ]
}


---

## ✅ SQL Safety

All generated SQL is:
- Parsed and validated using sqlglot
- Only SELECT queries are allowed
- All other query types (UPDATE, INSERT, DELETE, etc.) are blocked

---

## 📁 Project Structure


app/
├── api/routes/query.py       # POST /api/query route
├── core/llm.py               # ChatGPT call logic + schema context
├── core/sql_validation.py    # sqlglot-based validation
├── db/engine.py              # SQLAlchemy engine + DB connection
├── middleware/error.py       # Global exception handling
├── models/query.py           # Request/Response schemas
├── main.py                   # FastAPI app entry


---

## 📜 License

MIT – use freely, share knowledge.