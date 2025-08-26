import re
from openai import AsyncOpenAI
from app.core.settings import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a helpful assistant that converts natural language into SQL queries.
Only Generate SELECT statements thaat follow the given MYSQL Schema.
**DO NOT EXPLAIN ANYTHING ONLY OUTPUT THE SQL QUERY AND NOTHING ELSE**
"""
def build_prompt(nl_question: str, schema_str: str) -> list:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Schema:\n{schema_str}"},
        {"role": "user", "content": f"Question:\n{nl_question}"}
    ]
def clean_sql_output(raw: str) -> str:
    return re.sub(r"^```sql\s*|```$", "", raw.strip(), flags=re.IGNORECASE | re.MULTILINE).strip()

async def generate_sql_from_nl(nl_question: str, schema_str: str) -> str:
    messages = build_prompt(nl_question, schema_str)
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300,
        temperature=0,
    )
    raw_sql = response.choices[0].message.content.strip()
    sql = clean_sql_output(raw_sql)
    return sql
    