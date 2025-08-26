from fastapi import FastAPI
from app.middleware.error import register_exception_handlers
from app.api.routes.query import router as query_router 

app = FastAPI(title="Text2SQL - Sakila")

# Global exception handler
register_exception_handlers(app)

# Routes
app.include_router(query_router, prefix="/api", tags=["query"])