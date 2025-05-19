from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from pydantic import EmailStr, SecretStr

env = os.getenv("ENV", "dev")
if env == "dev":
    dotenv_path = ".env"
else:
    dotenv_path = f".env.{env}"
load_dotenv(dotenv_path=dotenv_path, override=True)


class Settings(BaseSettings):
    PROJECT_NAME: str = "Service Base FastAPI"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@db:5432/service_base_dev",
    )
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    RESET_PASSWORD_TOKEN_SECRET: str = "SECRET"
    VERIFICATION_TOKEN_SECRET: str = "SECRET"
    JWT_SECRET: str = "SECRET"
    HASHIDS_MIN_LENGTH: int = 12
    HASHIDS_SALT: str = os.getenv("HASHIDS_SALT", "SECRET")
    S3_ENDPOINT: str = os.getenv("S3_ENDPOINT", "https://s3.amazonaws.com")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "admin")
    S3_SECRET_KEY: str = os.getenv("S3_SECRET_KEY", "password")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "fastapi-app-dev")

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: SecretStr = SecretStr(os.getenv("MAIL_PASSWORD", ""))
    MAIL_FROM: EmailStr = os.getenv("MAIL_FROM", "dev@example.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "1025"))
    MAIL_WEB_PORT: int = int(os.getenv("MAIL_WEB_PORT", "1080"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "service-base-sendria")
    MAIL_STARTTLS: bool = env == "prod"
    USE_CREDENTIALS: bool = env == "prod"
    VALIDATE_CERTS: bool = env == "prod"
    SECURE_COOKIES: bool = env == "prod"


print("Loading environment variables...")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
settings = Settings()
