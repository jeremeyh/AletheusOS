"""Tests for executor models."""

from pathlib import Path

from tools.maintenance.ruf012.executor import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionSummary,
)


def test_execution_result_serialization() -> None:
    result = ExecutionResult(
        path=Path("example.py"),
        candidate_name="Example.VALUES",
        status=ExecutionStatus.PREVIEWED,
        message="Preview completed.",
        validated=True,
    )

    payload = result.as_dict()

    assert payload["candidate_name"] == "Example.VALUES"
    assert payload["status"] == "previewed"
    assert payload["validated"] is True


def test_execution_summary_counts() -> None:
    summary = ExecutionSummary(
        results=(
            ExecutionResult(
                Path("a.py"),
                "A.ONE",
                ExecutionStatus.PREVIEWED,
                "",
                True,
            ),
            ExecutionResult(
                Path("b.py"),
                "B.TWO",
                ExecutionStatus.SKIPPED,
                "",
                False,
            ),
            ExecutionResult(
                Path("c.py"),
                "C.THREE",
                ExecutionStatus.FAILED,
                "",
                False,
            ),
        )
    )

    assert summary.previewed == 1
    assert summary.skipped == 1
    assert summary.failed == 1
    assert summary.total == 3
    assert summary.successful is False


def test_execution_summary_serialization() -> None:
    summary = ExecutionSummary(results=())

    payload = summary.as_dict()

    assert payload["total"] == 0
    assert payload["successful"] is True
