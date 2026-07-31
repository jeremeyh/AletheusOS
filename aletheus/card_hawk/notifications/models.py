"""
Card Hawk Notification Models

Genesis 13.19
"""

import time
from dataclasses import dataclass, field


@dataclass
class NotificationEvent:
    event_type: str

    title: str

    message: str

    priority: str = "normal"

    confidence: int = 0

    channels: list = field(default_factory=list)

    timestamp: float = field(default_factory=time.time)
