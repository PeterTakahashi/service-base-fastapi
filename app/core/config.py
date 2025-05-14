from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

env = os.getenv("ENV", "dev")
if env == "dev":
    dotenv_path = ".env"
else:
    dotenv_path = f".env.{env}"
load_dotenv(dotenv_path=dotenv_path, override=True)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Manga Translator"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@db:5432/manga_translator_dev",
    )
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "SECRET")
    DEEPL_AUTH_KEY: str = os.getenv("DEEPL_AUTH_KEY", "SECRET")
    RESET_PASSWORD_TOKEN_SECRET: str = "SECRET"
    VERIFICATION_TOKEN_SECRET: str = "SECRET"
    JWT_SECRET: str = "SECRET"
    HASHIDS_MIN_LENGTH: int = 12
    HASHIDS_SALT: str = os.getenv("HASHIDS_SALT", "SECRET")
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT", "https://s3.amazonaws.com")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "admin")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "password")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "fastapi-app-dev")
    MAX_CHARACTER_IMAGES_COUNT: int = 5


print("Loading environment variables...")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
settings = Settings()
