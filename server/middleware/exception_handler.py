from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


async def exception_handler(request: Request, exc: Exception):
    logger.exception(
        f"Unhandled exception while processing request {request.method} {request.url}: {exc}"
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
