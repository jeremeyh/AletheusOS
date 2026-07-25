"""
Card Hawk Portfolio Models

Genesis 13.5
"""

from dataclasses import dataclass


@dataclass
class PortfolioSnapshot:

    asset_count: int

    cost_basis: float

    estimated_value: float

    unrealized_gain: float

    roi_percent: float

    allocation: dict

    risk_profile: dict

