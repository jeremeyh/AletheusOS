import logging
from pathlib import Path

from config.settings import settings

_LOGGERS = {}

def get_logger(name: str = "system"):
    settings.ensure_directories()
    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(f"cardhawk.{name}")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        log_path = Path(settings.log_dir) / f"{name}.log"
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    _LOGGERS[name] = logger
    return logger
