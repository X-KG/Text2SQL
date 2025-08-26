from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class QueryRequest(BaseModel):
    nl_query: str
    max_rows: Optional[int]

class QueryResponse(BaseModel):
    sql_query: str 
    rows: List[Dict[str, str]] = []
    row_count: int
    