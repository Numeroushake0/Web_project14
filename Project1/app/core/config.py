from pydantic import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    CORS_ORIGINS: List[str] = []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @classmethod
    def parse_cors_origins(cls, value: str) -> List[str]:
        try:
            return json.loads(value)
        except Exception:
            return [i.strip() for i in value.split(",")]

settings = Settings()

if isinstance(settings.CORS_ORIGINS, str):
    settings.CORS_ORIGINS = Settings.parse_cors_origins(settings.CORS_ORIGINS)
