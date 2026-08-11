from pathlib import Path

from config.settings import settings
from registry.engine_registry import EngineRegistry
from registry.provider_registry import ProviderRegistry


class SystemHealth:
    """Health Dashboard™ checks core CardHawk OS™ subsystems."""

    @staticmethod
    def check():
        provider_registry = ProviderRegistry().register_alpha_defaults()
        engine_registry = EngineRegistry().register_alpha_defaults()

        checks = {
            "app": "online",
            "environment": settings.environment,
            "database_path": str(settings.database_path),
            "database_exists": Path(settings.database_path).exists(),
            "data_dir_exists": Path(settings.data_dir).exists(),
            "upload_dir_exists": Path(settings.upload_dir).exists(),
            "log_dir_exists": Path(settings.log_dir).exists(),
            "providers_registered": provider_registry.names(),
            "engines_registered": engine_registry.names(),
            "schema_version": settings.schema_version,
            "pipeline_version": settings.pipeline_version,
            "database_version": settings.database_version,
        }

        return checks
