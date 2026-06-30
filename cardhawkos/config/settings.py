from pathlib import Path


class Settings:
    """
    CardHawkOS Production Configuration™
    """

    APP_NAME = "CardHawkOS"
    VERSION = "1.0.0-dev"

    DB_PATH = "data/cardhawk.db"

    DATA_DIR = Path("data")
    LOG_DIR = Path("logs")
    UPLOAD_DIR = Path("uploads")
    ASSET_IMAGE_DIR = Path("uploads/assets")

    MARKETPLACE_REFRESH_INTERVAL_MINUTES = 60
    DEF_REFRESH_INTERVAL_MINUTES = 60
    PORTFOLIO_REFRESH_INTERVAL_MINUTES = 30

    FEATURE_FLAGS = {
        "marketplace_intelligence": True,
        "def_command_center": True,
        "event_bus": True,
        "runtime_orchestrator": True,
        "founder_copilot": True,
        "hawk_aeye": True,
    }

    @classmethod
    def ensure_dirs(cls):
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)
        cls.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        cls.ASSET_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def snapshot(cls):
        cls.ensure_dirs()

        return {
            "app_name": cls.APP_NAME,
            "version": cls.VERSION,
            "db_path": cls.DB_PATH,
            "marketplace_refresh_interval_minutes": cls.MARKETPLACE_REFRESH_INTERVAL_MINUTES,
            "def_refresh_interval_minutes": cls.DEF_REFRESH_INTERVAL_MINUTES,
            "portfolio_refresh_interval_minutes": cls.PORTFOLIO_REFRESH_INTERVAL_MINUTES,
            "feature_flags": cls.FEATURE_FLAGS,
        }
