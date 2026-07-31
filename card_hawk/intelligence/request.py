"""
Unified Intelligence Request

Genesis 14.14
"""

from dataclasses import dataclass


@dataclass
class IntelligenceRequest:
    request_type: str

    payload: dict
