from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class CatalystRecommendation:
    target: str
    recommendation: str
    impact: str = "medium"
    metadata: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class CatalystReport:
    status: str
    recommendations: list[CatalystRecommendation] = field(default_factory=list)
    optimized_routes: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
