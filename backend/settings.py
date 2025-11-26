from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration with environment overrides."""

    app_title: str = "Grade & What-If Tracker"
    app_version: str = "1.0"
    database_url: str = "sqlite:///./grades.db"
    allowed_origins: List[str] = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ]
    auto_create_tables: bool = True

    class Config:
        env_prefix = "GRADEAPP_"
        env_file = ".env"


# Singleton settings instance for the app
settings = Settings()
