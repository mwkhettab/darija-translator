import logging
import time
import uuid
from fastapi import Request, Response

logger = logging.getLogger("request_logger")


async def request_logger(
    request: Request,
    call_next,
) -> Response:
    request_id = uuid.uuid4().hex
    start_time = time.monotonic()

    try:
        response = await call_next(request)
    except Exception:
        duration = time.monotonic() - start_time
        logger.exception(
            f"request_failed "
            f"request_id={request_id} "
            f"method={request.method} "
            f"path={request.url.path} "
            f"duration={duration:.4f}s"
        )
        raise

    duration = time.monotonic() - start_time

    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"request_completed "
        f"request_id={request_id} "
        f"method={request.method} "
        f"path={request.url.path} "
        f"status={response.status_code} "
        f"duration={duration:.4f}s"
    )

    return response
