from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from utils.languages import get_supported_languages

router = APIRouter()


@router.get("/languages", dependencies=[Depends(RateLimiter(times=30, seconds=60))])
def languages():
    return get_supported_languages()
