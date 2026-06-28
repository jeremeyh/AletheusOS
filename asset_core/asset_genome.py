from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class AssetGenomeEvent:
    """
    Asset Genome™ Event

    A single lifecycle event in an asset's history.
    """
    event_type: str
    description: str
    value: Any = None
    metadata: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class AssetGenome:
    """
    Asset Genome™

    Living historical timeline for every asset.
    """
    events: list[AssetGenomeEvent] = field(default_factory=list)

    def add(self, event_type: str, description: str, value=None, metadata=None):
        event = AssetGenomeEvent(
            event_type=event_type,
            description=description,
            value=value,
            metadata=metadata or {},
        )
        self.events.append(event)
        return event

    def purchase(self, price: float):
        return self.add("PURCHASE", "Asset acquired.", price)

    def valuation(self, value: float):
        return self.add("VALUATION", "Asset valuation updated.", value)

    def thorx(self, score: float):
        return self.add("THORX", "THORᵡ™ score updated.", score)

    def note(self, text: str):
        return self.add("FOUNDER_NOTE", text)

    def to_list(self):
        return [event.__dict__ for event in self.events]
