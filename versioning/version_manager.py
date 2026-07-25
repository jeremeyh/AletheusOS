from config.settings import settings


class VersionManager:
    """Version Manager™ for CardHawk OS™ releases."""

    @staticmethod
    def info():
        return {
            "product": "CardHawk OS™",
            "release": "Alpha 2.3",
            "build": settings.build,
            "schema_version": settings.schema_version,
            "pipeline_version": settings.pipeline_version,
            "database_version": settings.database_version,
            "environment": settings.environment,
        }
