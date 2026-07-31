"""Kinekt™ Runtime Boundary Analyzer engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .analysis import analyze_boundaries
from .loader import load_object
from .models import BoundaryReport
from .reporting import write_reports


class BoundaryEngine:
    def __init__(
        self,
        dependency_report: Path,
        cohesion_report: Path,
        output: Path,
    ) -> None:
        self.dependency_report = dependency_report.resolve()
        self.cohesion_report = cohesion_report.resolve()
        self.output = output.resolve()

    def analyze(self) -> BoundaryReport:
        dependency = load_object(self.dependency_report)
        cohesion = load_object(self.cohesion_report)
        findings, pressure, unresolved = analyze_boundaries(
            dependency,
            cohesion,
        )

        report = BoundaryReport(
            generated_at=datetime.now(UTC).isoformat(),
            dependency_report=str(self.dependency_report),
            cohesion_report=str(self.cohesion_report),
            findings=findings,
            package_pressure=pressure,
            unresolved_relationships=unresolved,
        )
        write_reports(report, self.output)
        return report
