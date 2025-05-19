from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.startup import startup, shutdown
from app.v1.app import v1_app

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI server for the project.",
    version="1.0.0",
)

origins = [settings.FRONTEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI Applicatoin!"}


@app.get("/up")
def health_check():
    """
    Health check endpoint.
    """
    return {"message": "up"}


app.mount("/app/v1", v1_app)
