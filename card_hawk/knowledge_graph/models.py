"""
Knowledge Graph Models

Genesis 14.6
"""

from dataclasses import dataclass, field


@dataclass
class Entity:
    entity_id: str

    entity_type: str

    name: str

    metadata: dict = field(default_factory=dict)


@dataclass
class Relationship:
    source: str

    target: str

    relationship_type: str

    confidence: int
