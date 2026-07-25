"""
CardHawk OS™
Startup
"""

from core.bootstrap import bootstrap
from core.logging import logger
from core.metrics import metrics


def startup():

    logger.info("Starting CardHawk OS")

    bootstrap.boot()

    metrics.increment("startup_count")

    logger.info("Startup complete")
