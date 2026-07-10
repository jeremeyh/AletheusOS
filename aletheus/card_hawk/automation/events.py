"""
Card Hawk Intelligence Events

Genesis 13.10
"""


from dataclasses import dataclass
import time



@dataclass
class IntelligenceEvent:

    event_type: str

    asset_id: str

    priority: str

    payload: dict

    timestamp: float = time.time()

