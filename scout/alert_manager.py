from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ScoutAlert:
    title: str
    message: str
    severity: str = "Info"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class AlertManager:
    """Creates and stores Scout™ alerts."""

    def __init__(self):
        self.alerts: list[ScoutAlert] = []

    def create(self, title: str, message: str, severity: str = "Info"):
        alert = ScoutAlert(title=title, message=message, severity=severity)
        self.alerts.append(alert)
        return alert

    def strike_zone(self, candidate_title: str):
        return self.create(
            "Strike Zone™ Candidate",
            f"{candidate_title} requires founder review.",
            "High",
        )

    def all(self):
        return self.alerts
