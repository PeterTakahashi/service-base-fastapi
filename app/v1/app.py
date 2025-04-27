from fastapi import FastAPI
from app.v1.routers import api as api_router
from app.core.config import settings

v1_app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Version 1 of the Manga Translator API",
    version="1.0.0",
)

v1_app.include_router(api_router.api_router)
