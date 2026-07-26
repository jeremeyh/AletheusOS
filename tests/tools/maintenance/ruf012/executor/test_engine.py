"""Tests for execution engine."""

from pathlib import Path

from tools.maintenance.ruf012.executor.engine import ExecutionEngine
from tools.maintenance.ruf012.executor.models import ExecutionStatus
from tools.maintenance.ruf012.planner import (
    PlannedRewrite,
    PlanStatus,
)


def test_execute_ready() -> None:
    engine = ExecutionEngine()

    summary = engine.execute(
        (
            PlannedRewrite(
                Path("a.py"),
                "Example",
                "VALUES",
                10,
                PlanStatus.READY,
                "",
            ),
        )
    )

    assert summary.previewed == 1
    assert summary.failed == 0
    assert summary.results[0].status is ExecutionStatus.PREVIEWED


def test_execute_skipped() -> None:
    engine = ExecutionEngine()

    summary = engine.execute(
        (
            PlannedRewrite(
                Path("a.py"),
                "Example",
                "VALUES",
                10,
                PlanStatus.SKIPPED,
                "ignored",
            ),
        )
    )

    assert summary.skipped == 1
    assert summary.results[0].status is ExecutionStatus.SKIPPED


def test_execute_failed() -> None:
    engine = ExecutionEngine()

    summary = engine.execute(
        (
            PlannedRewrite(
                Path("a.py"),
                "Example",
                "VALUES",
                10,
                PlanStatus.FAILED,
                "parse failure",
            ),
        )
    )

    assert summary.failed == 1
    assert summary.results[0].status is ExecutionStatus.FAILED
