import logging

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


logger = logging.getLogger(__name__)


async def app_exception_handler(
    request: Request,
    exc: AppException
):
    logger.error(
        "Application error | path=%s | message=%s",
        request.url.path,
        exc.message
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.message
        }
    )


async def general_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(
        "Unhandled exception | path=%s",
        request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error"
        }
    )