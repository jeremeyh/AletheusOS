from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PipelineContext:
    """
    ORCHESTRATOR™ Pipeline Context

    Single object passed through the intelligence pipeline.
    """

    asset_id: int

    asset: dict = field(default_factory=dict)
    vision: dict = field(default_factory=dict)
    market: dict = field(default_factory=dict)
    thorx: dict = field(default_factory=dict)
    def_report: dict = field(default_factory=dict)
    nest: dict = field(default_factory=dict)
    falcon: dict = field(default_factory=dict)

    events: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    started_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    completed_at: str = ""

    def add_event(self, name, payload=None):
        self.events.append(
            {
                "name": name,
                "payload": payload or {},
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    def add_error(self, step, error):
        self.errors.append(
            {
                "step": step,
                "error": str(error),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    def set_metric(self, key, value):
        self.metrics[key] = value

    def complete(self):
        self.completed_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return {
            "asset_id": self.asset_id,
            "asset": self.asset,
            "vision": self.vision,
            "market": self.market,
            "thorx": self.thorx,
            "def_report": self.def_report,
            "nest": self.nest,
            "falcon": self.falcon,
            "events": self.events,
            "errors": self.errors,
            "metrics": self.metrics,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
        }
