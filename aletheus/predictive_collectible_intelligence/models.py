"""
Predictive Intelligence Models

Genesis 13.38
"""

from dataclasses import dataclass, field



@dataclass
class MarketForecast:


    asset_id: str

    direction: str

    confidence: int

    timeframe: str

    signals: dict = field(
        default_factory=dict
    )


