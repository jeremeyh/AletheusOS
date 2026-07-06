"""
Spectrum Platform Analyzer Models

Genesis 54.0
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List


class Severity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FindingType(str, Enum):
    DUPLICATION = "DUPLICATION"
    COUPLING = "COUPLING"
    BOUNDARY = "BOUNDARY"
    CIRCULAR_DEPENDENCY = "CIRCULAR_DEPENDENCY"
    GOD_OBJECT = "GOD_OBJECT"
    DEAD_CODE = "DEAD_CODE"
    TECHNICAL_DEBT = "TECHNICAL_DEBT"
    STRUCTURAL = "STRUCTURAL"


@dataclass
class PlatformFinding:

    finding_id: str

    finding_type: FindingType

    severity: Severity

    title: str

    description: str

    component: str

    recommendation: str

    evidence: List[str] = field(default_factory=list)

    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    def to_dict(self):

        return {
            "finding_id": self.finding_id,
            "finding_type": self.finding_type.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "component": self.component,
            "recommendation": self.recommendation,
            "evidence": self.evidence,
            "created_at": self.created_at,
        }


@dataclass
class PlatformScore:

    architecture: float = 100.0

    coupling: float = 100.0

    boundaries: float = 100.0

    maintainability: float = 100.0

    constitutional: float = 100.0

    security: float = 100.0

    health: float = 100.0

    def overall(self) -> float:

        values = [
            self.architecture,
            self.coupling,
            self.boundaries,
            self.maintainability,
            self.constitutional,
            self.security,
            self.health,
        ]

        return round(sum(values) / len(values), 2)

    def to_dict(self):

        return {
            "architecture": self.architecture,
            "coupling": self.coupling,
            "boundaries": self.boundaries,
            "maintainability": self.maintainability,
            "constitutional": self.constitutional,
            "security": self.security,
            "health": self.health,
            "overall": self.overall(),
        }


@dataclass
class PlatformReport:

    report_id: str

    generated_at: str

    score: PlatformScore

    findings: List[PlatformFinding] = field(default_factory=list)

    metadata: Dict = field(default_factory=dict)

    def to_dict(self):

        return {
            "report_id": self.report_id,
            "generated_at": self.generated_at,
            "score": self.score.to_dict(),
            "findings": [
                finding.to_dict()
                for finding in self.findings
            ],
            "metadata": self.metadata,
        }
