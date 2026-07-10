"""
Marketplace Intelligence Models

Genesis 13.41
"""

from dataclasses import dataclass, field



@dataclass
class MarketplaceConnector:


    name: str

    marketplace_type: str

    capabilities: list = field(
        default_factory=list
    )

    status: str = "active"



@dataclass
class MarketSignal:


    source: str

    signal_type: str

    value: dict

