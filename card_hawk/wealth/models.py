"""
Collectible Wealth Models

Genesis 14.27
"""

from dataclasses import dataclass


@dataclass
class PortfolioMetric:
    name: str

    value: float


@dataclass
class AssetPerformance:
    asset_id: str

    gain: float
