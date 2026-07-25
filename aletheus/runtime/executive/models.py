from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class ExecutiveDecision:
    action: str
    status: str
    reason: str = ""
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class ExecutiveState:
    status: str = "initialized"
    active_missions: list[str] = field(default_factory=list)
    active_services: list[str] = field(default_factory=list)
    last_decision: ExecutiveDecision | None = None
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
