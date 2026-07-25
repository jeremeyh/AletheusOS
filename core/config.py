"""
CardHawk OS™
Configuration Manager
"""

import os
from pathlib import Path


class Config:

    ROOT = Path(__file__).resolve().parent.parent

    DEBUG = os.getenv("CARDHAWK_DEBUG", "false").lower() == "true"

    DATABASE_PATH = ROOT / "data" / "cardhawk.db"

    LOG_LEVEL = os.getenv("CARDHAWK_LOG_LEVEL", "INFO")

    FEATURE_FLAGS = {
        "hawk_aeye": True,
        "thorx": True,
        "founder_ai": True,
        "continuous_scout": True,
        "adaptive_intelligence": True,
        "live_data": False,
        "commercialization": False,
    }

config = Config()
