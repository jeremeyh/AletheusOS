"""
CardHawk OS™
Startup
"""

from core.logging import logger
from core.bootstrap import bootstrap
from core.metrics import metrics

def startup():

    logger.info("Starting CardHawk OS")

    bootstrap.boot()

    metrics.increment("startup_count")

    logger.info("Startup complete")
