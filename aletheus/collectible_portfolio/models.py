"""
Portfolio Intelligence Models

Genesis 13.33
"""

from dataclasses import dataclass, field


@dataclass
class PortfolioSnapshot:
    total_assets: int

    estimated_value: float

    categories: dict = field(default_factory=dict)

    metrics: dict = field(default_factory=dict)
