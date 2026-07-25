from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum


class VerificationStatus(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class VerificationResult:
    name: str
    status: VerificationStatus
    summary: str
    duration_seconds: float = 0.0
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())


@dataclass
class PlatformVerificationReport:
    results: list[VerificationResult] = field(default_factory=list)

    def passed(self) -> bool:
        return all(r.status != VerificationStatus.FAIL for r in self.results)

    def health_score(self) -> float:
        if not self.results:
            return 0.0
        score = 0
        for result in self.results:
            if result.status == VerificationStatus.PASS:
                score += 1
            elif result.status == VerificationStatus.WARN:
                score += 0.5
        return round((score / len(self.results)) * 100, 2)
