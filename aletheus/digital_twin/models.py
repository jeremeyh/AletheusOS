"""
Digital Twin Models

Genesis 13.49
"""

from dataclasses import dataclass, field


@dataclass
class DigitalTwin:
    entity_id: str

    entity_type: str

    state: dict = field(default_factory=dict)

    scenarios: list = field(default_factory=list)
