"""
Market Intelligence Models

Genesis 14.13
"""

from dataclasses import dataclass, field



@dataclass
class MarketSignal:


    asset_id: str

    signal_type: str

    value: float



@dataclass
class Forecast:


    asset_id: str

    prediction: str

    confidence: int

