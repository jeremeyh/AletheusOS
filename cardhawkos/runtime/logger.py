from datetime import datetime
from pathlib import Path


class CardHawkLogger:
    LOG_DIR = Path("logs")
    LOG_FILE = LOG_DIR / "cardhawkos.log"

    @classmethod
    def write(cls, level, message):
        cls.LOG_DIR.mkdir(parents=True, exist_ok=True)

        line = (
            f"{datetime.utcnow().isoformat()} "
            f"[{level.upper()}] "
            f"{message}\n"
        )

        with open(cls.LOG_FILE, "a") as f:
            f.write(line)

    @classmethod
    def info(cls, message):
        cls.write("INFO", message)

    @classmethod
    def warning(cls, message):
        cls.write("WARNING", message)

    @classmethod
    def error(cls, message):
        cls.write("ERROR", message)
