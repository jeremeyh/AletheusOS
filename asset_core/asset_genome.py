from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GenomeEvent:
    """
    A single event in an asset's lifecycle.
    """

    timestamp: str
    event: str
    source: str
    details: str


@dataclass
class AssetGenome:
    """
    Living historical timeline for every CardHawk asset.

    Every significant event is permanently recorded.
    """

    asset_uuid: str

    timeline: list[GenomeEvent] = field(default_factory=list)

    def add_event(
        self,
        event,
        source,
        details,
    ):

        self.timeline.append(
            GenomeEvent(
                timestamp=datetime.utcnow().isoformat(),
                event=event,
                source=source,
                details=details,
            )
        )

    def history(self):

        return self.timeline
