"""Kinekt™ repository intelligence engine."""

from __future__ import annotations

from datetime import UTC, datetime

from .analyzers import (
    boundary_findings,
    duplicate_findings,
    orphan_findings,
    syntax_findings,
)
from .configuration import KinektConfiguration
from .graph import RepositoryGraph
from .metrics import calculate_package_metrics
from .models import AnalysisResult
from .reporting import write_reports
from .scanner import scan_repository


class KinektEngine:
    def __init__(self, configuration: KinektConfiguration) -> None:
        self.configuration = configuration

    def analyze(self) -> AnalysisResult:
        modules = scan_repository(self.configuration)
        graph = RepositoryGraph(modules)

        findings = [
            *syntax_findings(modules),
            *boundary_findings(modules, self.configuration.boundary_rules),
            *duplicate_findings(modules),
            *orphan_findings(modules, graph),
        ]
        findings.sort(key=lambda item: (item.severity, item.code, item.subject))

        result = AnalysisResult(
            root=str(self.configuration.root.resolve()),
            generated_at=datetime.now(UTC).isoformat(),
            modules=modules,
            findings=findings,
            package_metrics=calculate_package_metrics(modules, graph, findings),
        )
        write_reports(result, self.configuration.output.resolve())
        return result
