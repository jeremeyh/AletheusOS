"""Kinekt™ Constitutional Dependency Graph engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .builder import build_dependency_graph
from .loader import load_object
from .models import DependencyGraphReport
from .reporting import write_reports


class DependencyEngine:
    def __init__(
        self,
        repository_report: Path,
        topology_report: Path,
        output: Path,
    ) -> None:
        self.repository_report = repository_report.resolve()
        self.topology_report = topology_report.resolve()
        self.output = output.resolve()

    def analyze(self) -> DependencyGraphReport:
        repository = load_object(self.repository_report)
        topology = load_object(self.topology_report)

        nodes, relationships, findings, unresolved = build_dependency_graph(
            repository,
            topology,
        )

        report = DependencyGraphReport(
            generated_at=datetime.now(UTC).isoformat(),
            repository_report=str(self.repository_report),
            topology_report=str(self.topology_report),
            nodes=nodes,
            relationships=relationships,
            findings=findings,
            unresolved_modules=unresolved,
        )
        write_reports(report, self.output)
        return report
