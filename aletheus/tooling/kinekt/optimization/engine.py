"""Kinekt™ Optimization Planner engine."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .loader import load_object
from .models import OptimizationPlan
from .planner import build_work_packages, candidates_from_reports
from .reporting import write_reports


class OptimizationEngine:
    def __init__(
        self,
        resolution_report: Path,
        integrity_report: Path,
        dependency_report: Path,
        cohesion_report: Path,
        boundary_report: Path,
        health_report: Path,
        output: Path,
    ) -> None:
        self.paths = {
            "resolution": resolution_report.resolve(),
            "integrity": integrity_report.resolve(),
            "dependency": dependency_report.resolve(),
            "cohesion": cohesion_report.resolve(),
            "boundary": boundary_report.resolve(),
            "health": health_report.resolve(),
        }
        self.output = output.resolve()

    def analyze(self) -> OptimizationPlan:
        reports = {name: load_object(path) for name, path in self.paths.items()}
        candidates, abstentions = candidates_from_reports(
            reports["resolution"],
            reports["dependency"],
            reports["cohesion"],
            reports["boundary"],
            reports["health"],
        )
        work_packages = build_work_packages(candidates)
        quick_wins = [
            item.candidate_id
            for item in candidates
            if item.effort in {"low", "medium"}
            and item.risk == "low"
            and item.confidence >= 0.75
            and item.expected_health_gain > 0
        ]
        plan = OptimizationPlan(
            generated_at=datetime.now(UTC).isoformat(),
            current_health_score=float(reports["health"].get("total_score", 0.0)),
            readiness=str(reports["health"].get("readiness", "unknown")),
            candidates=candidates,
            work_packages=work_packages,
            quick_wins=quick_wins,
            abstentions=abstentions,
            provenance={name: str(path) for name, path in self.paths.items()},
        )
        write_reports(plan, self.output)
        return plan
