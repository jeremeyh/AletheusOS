from dataclasses import dataclass, field
from datetime import UTC, datetime


@dataclass
class RuntimeShimReport:
    """
    Runtime Core Shim delegation report.

    Records when responsibilities have been delegated from the legacy
    runtime core to the compositional runtime architecture.
    """

    status: str
    delegated_services: list[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(UTC).isoformat()
    )
