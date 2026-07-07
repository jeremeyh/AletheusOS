from __future__ import annotations

from .models import ConceptSignature
from .service import ConceptCollisionService


class ConceptCollisionAPI:
    """Thin API layer for future runtime/service-bus exposure."""

    def __init__(self, service: ConceptCollisionService) -> None:
        self.service = service

    def evaluate(self, payload: dict) -> dict:
        candidate = ConceptSignature(**payload)
        report = self.service.evaluate(candidate)
        return {
            "passed": report.passed,
            "summary": report.summary,
            "findings": [
                {
                    "target": finding.target.name,
                    "type": finding.collision_type.value,
                    "severity": finding.severity.value,
                    "confidence": finding.confidence,
                    "recommended_outcome": finding.recommended_outcome.value,
                    "rationale": finding.rationale,
                    "requires_adr": finding.requires_adr,
                }
                for finding in report.findings
            ],
        }
