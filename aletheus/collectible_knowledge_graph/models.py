"""
Knowledge Graph Models

Genesis 13.37
"""

from dataclasses import dataclass, field


@dataclass
class GraphEntity:


    entity_id: str

    entity_type: str

    name: str

    attributes: dict = field(
        default_factory=dict
    )



@dataclass
class GraphRelationship:


    source: str

    relationship: str

    target: str

