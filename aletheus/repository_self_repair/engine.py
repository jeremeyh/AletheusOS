from __future__ import annotations

import time
from pathlib import Path

from .executor import RepairExecutor
from .models import ExecutionResult, RepairPlan, ScanManifest
from .planner import RepairPlanner
from .policy import RepairPolicy
from .reporter import RepairReporter
from .scanner import RepositoryScanner


class RepositorySelfRepairEngine:
    def __init__(self, policy: RepairPolicy | None = None) -> None:
        self.policy = policy or RepairPolicy.default()
        self.scanner = RepositoryScanner(self.policy)
        self.planner = RepairPlanner(self.policy)
        self.executor = RepairExecutor()

    def diagnose(
        self, target: Path, source: Path | None = None
    ) -> tuple[ScanManifest, ScanManifest | None, RepairPlan]:
        target_manifest = self.scanner.scan(target)
        source_manifest = self.scanner.scan(source) if source else None
        plan = self.planner.plan(target_manifest, source_manifest)
        return target_manifest, source_manifest, plan

    def run(
        self,
        target: Path,
        source: Path | None = None,
        *,
        apply: bool = False,
        delete_known_orphans: bool = False,
        archive_source: bool = False,
        remove_source: bool = False,
        archive_root: Path | None = None,
        report_root: Path | None = None,
    ) -> tuple[RepairPlan, ExecutionResult, Path]:
        target_manifest, _, plan = self.diagnose(target, source)
        result = self.executor.execute(
            plan,
            dry_run=not apply,
            delete_known_orphans=delete_known_orphans,
            archive_source=archive_source,
            remove_source=remove_source,
            archive_root=archive_root,
        )
        report_root = (
            report_root or Path(target).resolve() / "reports" / "repository_self_repair"
        )
        report_path = RepairReporter(report_root).write(target_manifest, plan, result)
        return plan, result, report_path

    def monitor(
        self,
        target: Path,
        *,
        interval_seconds: int = 3600,
        report_root: Path | None = None,
    ) -> None:
        if interval_seconds < 60:
            raise ValueError("monitor interval must be at least 60 seconds")
        while True:
            # Continuous mode is intentionally non-destructive. It diagnoses and
            # quarantines only known debris; repository convergence remains explicit.
            self.run(target, apply=True, report_root=report_root)
            time.sleep(interval_seconds)
