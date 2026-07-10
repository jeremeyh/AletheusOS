"""
Discovery Mission Models

Genesis 13.25
"""

from dataclasses import dataclass, field



@dataclass
class DiscoveryMission:


    mission_id: str

    name: str

    category: str

    query: str

    sources: list = field(
        default_factory=list
    )

    filters: dict = field(
        default_factory=dict
    )

    intelligence_rules: dict = field(
        default_factory=dict
    )

    status: str = "created"

