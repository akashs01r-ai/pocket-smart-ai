from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "PocketSmart AI")

    environment: str = os.getenv(
        "ENVIRONMENT",
        "development",
    )

    secret_key: str = os.getenv(
        "SECRET_KEY",
        "change-this-secret-key",
    )

    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/pocketsmart.db",
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        "",
    )

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash",
    )

    jwt_expire_minutes: int = int(
        os.getenv(
            "JWT_EXPIRE_MINUTES",
            "1440",
        )
    )

    max_upload_mb: int = int(
        os.getenv(
            "MAX_UPLOAD_MB",
            "5",
        )
    )

    allowed_origins: str = os.getenv(
        "ALLOWED_ORIGINS",
        "http://127.0.0.1:8000,http://localhost:8000",
    )

    @property
    def origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]

    @property
    def database_path(self) -> Path:
        if not self.database_url.startswith("sqlite:///"):
            raise ValueError(
                "This version of PocketSmart AI uses SQLite."
            )

        raw_path = self.database_url.replace(
            "sqlite:///",
            "",
            1,
        )

        path = Path(raw_path)

        if not path.is_absolute():
            path = BASE_DIR / path

        return path


@lru_cache
def get_settings() -> Settings:
    return Settings()