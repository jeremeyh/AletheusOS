from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .loader import load_object
from .models import ObservatoryAlert, ObservatoryReport
from .reporting import write_reports


class ObservatoryEngine:
    def __init__(
        self,
        health: Path,
        authority: Path,
        twin: Path,
        orchestration: Path,
        output: Path,
    ) -> None:
        self.paths = {
            "health": health.resolve(),
            "authority": authority.resolve(),
            "twin": twin.resolve(),
            "orchestration": orchestration.resolve(),
        }
        self.output = output.resolve()

    def analyze(self) -> ObservatoryReport:
        reports = {name: load_object(path) for name, path in self.paths.items()}
        health_score = float(reports["health"].get("total_score", 0.0))
        readiness = str(reports["health"].get("readiness", "unknown"))
        assignments = reports["authority"].get("module_assignments", {})
        unresolved = reports["authority"].get("unresolved_modules", [])
        assigned_count = len(assignments) if isinstance(assignments, dict) else 0
        unresolved_count = len(unresolved) if isinstance(unresolved, list) else 0
        coverage = round(
            assigned_count / max(1, assigned_count + unresolved_count) * 100.0,
            2,
        )
        units = reports["orchestration"].get("units", [])
        execution_units = len(units) if isinstance(units, list) else 0

        alerts: list[ObservatoryAlert] = []
        if health_score < 60:
            alerts.append(
                ObservatoryAlert(
                    code="CONSTITUTIONAL_HEALTH_CRITICAL",
                    severity="critical",
                    message=f"Constitutional health is {health_score:.2f}.",
                    evidence=(str(self.paths["health"]),),
                )
            )
        if coverage < 50:
            alerts.append(
                ObservatoryAlert(
                    code="AUTHORITY_COVERAGE_LOW",
                    severity="high",
                    message=f"Capability authority coverage is {coverage:.2f}%.",
                    evidence=(str(self.paths["authority"]),),
                )
            )
        if readiness == "not_ready":
            alerts.append(
                ObservatoryAlert(
                    code="PLATFORM_NOT_READY",
                    severity="high",
                    message="Kinekt constitutional readiness is not_ready.",
                )
            )

        report = ObservatoryReport(
            generated_at=datetime.now(UTC).isoformat(),
            health_score=health_score,
            readiness=readiness,
            authority_coverage=coverage,
            unresolved_modules=unresolved_count,
            execution_units=execution_units,
            alerts=alerts,
            provenance={name: str(path) for name, path in self.paths.items()},
        )
        write_reports(report, self.output)
        return report
