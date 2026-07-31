"""Kinekt™ Constitutional Health engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .loader import load_object
from .models import HealthReport
from .reporting import write_reports
from .scoring import build_dimensions, readiness, status, total_score


class HealthEngine:
    def __init__(
        self,
        integrity_report: Path,
        topology_report: Path,
        dependency_report: Path,
        cohesion_report: Path,
        boundary_report: Path,
        output: Path,
    ) -> None:
        self.integrity_report = integrity_report.resolve()
        self.topology_report = topology_report.resolve()
        self.dependency_report = dependency_report.resolve()
        self.cohesion_report = cohesion_report.resolve()
        self.boundary_report = boundary_report.resolve()
        self.output = output.resolve()

    def analyze(self) -> HealthReport:
        integrity = load_object(self.integrity_report)
        topology = load_object(self.topology_report)
        dependency = load_object(self.dependency_report)
        cohesion = load_object(self.cohesion_report)
        boundary = load_object(self.boundary_report)

        dimensions = build_dimensions(
            integrity,
            topology,
            dependency,
            cohesion,
            boundary,
        )
        score = total_score(dimensions)
        risks = sorted({risk for dimension in dimensions for risk in dimension.risks})

        report = HealthReport(
            generated_at=datetime.now(UTC).isoformat(),
            total_score=score,
            status=status(score),
            readiness=readiness(score, dimensions),
            dimensions=dimensions,
            top_risks=risks,
            provenance={
                "integrity": str(self.integrity_report),
                "topology": str(self.topology_report),
                "dependency": str(self.dependency_report),
                "cohesion": str(self.cohesion_report),
                "boundary": str(self.boundary_report),
            },
        )
        write_reports(report, self.output)
        return report
