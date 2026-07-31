"""
Card Hawk Intelligence Events

Genesis 13.10
"""

import time
from dataclasses import dataclass


@dataclass
class IntelligenceEvent:
    event_type: str

    asset_id: str

    priority: str

    payload: dict

    timestamp: float = time.time()
