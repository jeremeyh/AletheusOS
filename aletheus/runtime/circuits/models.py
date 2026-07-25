from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class RuntimeCircuit:
    name: str
    capability: str
    status: str = "detached"
    dependencies: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class CircuitActivationResult:
    circuit: str
    status: str
    message: str = ""
    metadata: dict = field(default_factory=dict)
    completed_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
