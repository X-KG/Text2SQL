from sqlglot import parse_one, expressions
from sqlglot.errors import ParseError

def validate_sql(query: str) -> bool:
    try:
        parsed = parse_one(query, read="mysql")
    except ParseError as e:
        raise ValueError(f"Invalid SQL query: {e}")
    if not isinstance(parsed, expressions.Select):
        raise ValueError("Only SELECT statements are allowed.")
    print("Valid SQL query.")
    return True