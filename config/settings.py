from dataclasses import dataclass
from pathlib import Path

from config.constants import (
    APP_NAME,
    APP_VERSION,
    BUILD,
    DATABASE_VERSION,
    PIPELINE_VERSION,
    SCHEMA_VERSION,
)


@dataclass
class Settings:
    app_name: str = APP_NAME
    app_version: str = APP_VERSION
    build: str = BUILD
    schema_version: str = SCHEMA_VERSION
    pipeline_version: str = PIPELINE_VERSION
    database_version: str = DATABASE_VERSION

    environment: str = "development"
    data_dir: Path = Path("data")
    upload_dir: Path = Path("uploads")
    log_dir: Path = Path("logs")
    database_path: Path = Path("data/cardhawk.db")

    canonical_engine_package: str = "engines"
    deprecated_engine_package: str = "engine"

    def ensure_directories(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_directories()
