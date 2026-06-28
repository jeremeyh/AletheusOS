from pathlib import Path

class ConfigValidator:
    """Configuration validation and startup integrity checks."""

    REQUIRED_DIRS = ["data", "uploads", "logs"]

    @staticmethod
    def validate():
        results = {}
        for folder in ConfigValidator.REQUIRED_DIRS:
            path = Path(folder)
            path.mkdir(parents=True, exist_ok=True)
            results[folder] = path.exists()
        return results
