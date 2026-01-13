from typing import Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_limiter.depends import RateLimiter

from schemas.request import TranslateRequest
from schemas.response import (
    TranslateMultiTextResponse,
    TranslateSingleTextResponse,
)
from services.translation.service import translate_text
from utils.languages import is_supported_language

router = APIRouter()


@router.post(
    "/translate",
    dependencies=[Depends(RateLimiter(times=100, seconds=86400))],
)
def translate(
    request: TranslateRequest,
) -> Union[TranslateSingleTextResponse, TranslateMultiTextResponse]:
    source = request.source_language
    target = request.target_language

    if not is_supported_language(source) or not is_supported_language(target):
        return JSONResponse(
            status_code=400,
            content={
                "detail": (
                    f"Unsupported language code: {source} or {target}. "
                    "Try /api/languages for supported codes."
                )
            },
        )

    if source != "ary" and target != "ary":
        return JSONResponse(
            status_code=400,
            content={"detail": "One of the languages must be Darija (ary)."},
        )
    try:
        return translate_text(
            source_language=source,
            target_language=target,
            text=request.text,
        )
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
