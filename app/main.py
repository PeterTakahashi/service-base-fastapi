import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.startup import startup, shutdown
from app.v1.app import v1_app

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A FastAPI server for manga translation",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

@app.get("/")
def root():
    return {"message": "Welcome to the Manga Translator API!"}

@app.get("/up")
def health_check():
    """
    Health check endpoint.
    """
    return {"message": "up"}

app.mount("/app/v1", v1_app)
