import os
import logging
from contextlib import asynccontextmanager
import asyncio

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter

from services.translation.hf_client import init_models
from api.health import router as health_router
from api.languages import router as languages_router
from api.translate import router as translate_router
from core.config import settings
from core.logging import setup_logging
from middleware.exception_handler import exception_handler
from middleware.request_logger import request_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting app...")
    
    logging.info("Initializing models...")
    init_models()
    
    logging.info("Setting up Redis for rate limiting...")
    redis_client = None

    try:
        redis_client = redis.from_url(
            str(settings.redis_url),
            encoding="utf-8",
            decode_responses=True,
        )
        await FastAPILimiter.init(redis_client)
    except Exception as exc:
        logging.warning("Redis unavailable, API will return 500", exc_info=exc)

    logging.info("App started.")
    yield

    if redis_client:
        await redis_client.close()

    logging.info("App shutdown complete.")


def create_app() -> FastAPI:
    try:
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        setup_logging(settings.environment)

        logging.info("Creating FastAPI app...")
        app = FastAPI(
            title="Darija Translator API",
            lifespan=lifespan,
        )

        app.add_exception_handler(Exception, exception_handler)

        app.add_middleware(
            CORSMiddleware,
            allow_origins=[origin.strip() for origin in str(settings.cors_allowed_origins).split(",")],
            allow_methods=["*"],
        )

        app.middleware("http")(request_logger)

        app.include_router(health_router, prefix="/api")
        app.include_router(languages_router, prefix="/api")
        app.include_router(translate_router, prefix="/api")

        logging.info("FastAPI app is ready.")
        return app
    except Exception as e:
        logging.critical("Failed to create FastAPI app.", exc_info=e)
        raise


app = create_app()
