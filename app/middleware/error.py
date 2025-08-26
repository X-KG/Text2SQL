# app/middleware/error.py

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import logging

logger = logging.getLogger(__name__)


def register_exception_handlers(app):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.warning(f"{exc.status_code} error: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "errMsg": str(exc.detail),
                "response": None,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(f"422 Validation error: {exc.errors()}")
        errors = []
        for e in exc.errors():
            loc = ".".join(str(p) for p in e.get("loc", []))
            msg = e.get("msg", "Invalid input")
            errors.append({"field": loc, "msg": msg})

        return JSONResponse(
            status_code=422,
            content={
                "status": 422,
                "errMsg": "Validation failed",
                "response": None,
                "errors": errors,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"500 Internal Server Error: {exc}", exc_info=True)
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status": 500,
                "errMsg": "Internal Server Error",
                "response": None,
            },
        )