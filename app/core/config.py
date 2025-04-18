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
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY")
    DEEPL_AUTH_KEY: str = os.getenv("DEEPL_AUTH_KEY")
    RESET_PASSWORD_TOKEN_SECRET: str = "SECRET"
    VERIFICATION_TOKEN_SECRET: str = "SECRET"
    JWT_SECRET: str = "SECRET"

print("Loading environment variables...")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
settings = Settings()
