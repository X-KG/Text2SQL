from fastapi import APIRouter, Body, HTTPException
from sqlalchemy import text
from app.models.query import QueryRequest, QueryResponse
from app.core.llm import generate_sql_from_nl
from app.core.sql_validation import validate_sql
from app.db.engine import SessionLocal 

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def query_handler(request: QueryRequest = Body(...)):
    schema_str = """
    customer(customer_id, store_id, first_name, last_name, email, address_id, active, create_date, last_update)
    """

    try:
        # Get SQL from NL
        sql_query = await generate_sql_from_nl(request.nl_query, schema_str)

        # Validate SQL (to be SELECT)
        validate_sql(sql_query)

        # Execute query on DB
        async with SessionLocal() as session:
            stmt = text(sql_query).execution_options(populate_existing=True)
            result = await session.execute(stmt)
            rows = result.fetchall()

            # Limit result to max_rows from request
            limited_rows = [dict(row._mapping) for row in rows[:request.max_rows]]

        return QueryResponse(
            sql_query=sql_query,
            rows=limited_rows,
            row_count=len(limited_rows)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM or DB error: {str(e)}")