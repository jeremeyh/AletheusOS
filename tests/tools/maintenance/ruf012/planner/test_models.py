"""Tests for planner models."""

from pathlib import Path

from tools.maintenance.ruf012.planner import (
    PlannedRewrite,
    PlannerSummary,
    PlanStatus,
)


def test_candidate_name() -> None:
    rewrite = PlannedRewrite(
        path=Path("example.py"),
        class_name="Example",
        attribute_name="VALUES",
        line_number=4,
        status=PlanStatus.READY,
        reason="safe",
    )

    assert rewrite.candidate_name == "Example.VALUES"


def test_serialization() -> None:
    rewrite = PlannedRewrite(
        path=Path("example.py"),
        class_name="Example",
        attribute_name="VALUES",
        line_number=4,
        status=PlanStatus.READY,
        reason="safe",
    )

    payload = rewrite.as_dict()

    assert payload["candidate_name"] == "Example.VALUES"
    assert payload["status"] == "ready"


def test_summary_counts() -> None:
    summary = PlannerSummary(
        rewrites=(
            PlannedRewrite(
                Path("a.py"),
                "A",
                "ONE",
                1,
                PlanStatus.READY,
                "",
            ),
            PlannedRewrite(
                Path("b.py"),
                "B",
                "TWO",
                2,
                PlanStatus.SKIPPED,
                "",
            ),
            PlannedRewrite(
                Path("c.py"),
                "C",
                "THREE",
                3,
                PlanStatus.FAILED,
                "",
            ),
        )
    )

    assert summary.ready == 1
    assert summary.skipped == 1
    assert summary.failed == 1
    assert summary.total == 3
    assert summary.successful is False


def test_summary_serialization() -> None:
    summary = PlannerSummary(rewrites=())

    payload = summary.as_dict()

    assert payload["total"] == 0
    assert payload["successful"] is True
