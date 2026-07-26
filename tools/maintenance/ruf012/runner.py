"""
Genesis 11 native RUF012 runner.

Coordinates repository discovery, extraction, planning,
preview execution, and reporting.
"""

from __future__ import annotations

from pathlib import Path

from tools.maintenance.ruf012.executor.engine import ExecutionEngine
from tools.maintenance.ruf012.extractor import RUF012CandidateExtractor
from tools.maintenance.ruf012.planner.planner import PlannerEngine
from tools.maintenance.ruf012.scanner import RepositoryScanner
from tools.maintenance.ruf012.writer import RepositoryWriter


class Runner:
    """Native orchestration entry point."""

    def __init__(
        self,
        root: Path | str = ".",
    ) -> None:
        self.root = Path(root).resolve()

    def run(self) -> int:
        """Execute the native preview pipeline."""

        scanner = RepositoryScanner(self.root)
        scan = scanner.scan()

        extractor = RUF012CandidateExtractor()
        extraction = extractor.extract_paths(
            paths=scan.python_files,
        )

        planner = PlannerEngine()
        plan = planner.build_plan(
            candidates=extraction.candidates,
            failures=extraction.failures,
        )

        executor = ExecutionEngine()
        execution = executor.execute(plan.rewrites)

        writer = RepositoryWriter(self.root)
        writer.apply(execution)

        print()
        print("=" * 72)
        print("Genesis 11 Native Pipeline")
        print("=" * 72)
        print(f"Repository           : {self.root}")
        print(f"Python files         : {scan.files_discovered}")
        print(f"Candidates           : {extraction.candidates_discovered}")
        print(f"Extraction failures  : {extraction.failed_files}")
        print(f"Ready                : {plan.ready}")
        print(f"Skipped              : {plan.skipped}")
        print(f"Planning failures    : {plan.failed}")
        print(f"Previewed            : {execution.previewed}")
        print(f"Execution failures   : {execution.failed}")

        return 0 if execution.successful else 1
