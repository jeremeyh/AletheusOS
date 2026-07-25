from migrations.migration_runner import MigrationRunner
from security.config_validator import ConfigValidator
from versioning.version_manager import VersionManager


class StartupVerifier:
    """Startup Verification™."""

    @staticmethod
    def verify(run_migrations=False):
        config = ConfigValidator.validate()
        migrations = []
        if run_migrations:
            migrations = MigrationRunner().run()

        return {
            "config": config,
            "migrations_applied": migrations,
            "version": VersionManager.info() if hasattr(VersionManager, "info") else {},
            "status": "ready",
        }
