"""
Portfolio Models

Genesis 14.2
"""

from dataclasses import dataclass, field


@dataclass
class PortfolioSnapshot:


    total_cost: float

    current_value: float

    assets: list = field(
        default_factory=list
    )



@dataclass
class AssetPerformance:


    asset_id: str

    cost_basis: float

    current_value: float

    thesis: str = ""

