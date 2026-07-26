"""Tests for PlannerEngine."""

from pathlib import Path

from tools.maintenance.ruf012.extractor import (
    CandidateClassification,
    ExtractedCandidate,
    ExtractionFailure,
    MutableValueKind,
)
from tools.maintenance.ruf012.planner.models import PlanStatus
from tools.maintenance.ruf012.planner.planner import PlannerEngine


def test_safe_candidate_is_ready() -> None:
    planner = PlannerEngine()

    summary = planner.build_plan(
        (
            ExtractedCandidate(
                path=Path("a.py"),
                class_name="Example",
                attribute_name="VALUES",
                line_number=10,
                column_offset=0,
                classification=CandidateClassification.SAFE,
                value_kind=MutableValueKind.LIST,
                reason="",
            ),
        )
    )

    rewrite = summary.rewrites[0]

    assert rewrite.status is PlanStatus.READY
    assert rewrite.reason == ""


def test_non_safe_candidate_is_skipped() -> None:
    planner = PlannerEngine()

    summary = planner.build_plan(
        (
            ExtractedCandidate(
                path=Path("a.py"),
                class_name="Example",
                attribute_name="VALUES",
                line_number=10,
                column_offset=0,
                classification=CandidateClassification.UNSUPPORTED,
                value_kind=MutableValueKind.LIST,
                reason="Unsupported assignment.",
            ),
        )
    )

    rewrite = summary.rewrites[0]

    assert rewrite.status is PlanStatus.SKIPPED
    assert rewrite.reason == "Unsupported assignment."


def test_failure_becomes_failed_plan() -> None:
    planner = PlannerEngine()

    summary = planner.build_plan(
        (),
        (
            ExtractionFailure(
                path=Path("broken.py"),
                error="Syntax error.",
            ),
        ),
    )

    rewrite = summary.rewrites[0]

    assert rewrite.status is PlanStatus.FAILED
    assert rewrite.reason == "Syntax error."
