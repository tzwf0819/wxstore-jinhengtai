from fastapi import FastAPI
from loguru import logger

from .api import api_router
from .core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name, debug=settings.debug)
app.include_router(api_router)


@app.on_event("startup")
async def startup_event() -> None:
    logger.info("Starting FastAPI application: {}", settings.app_name)
