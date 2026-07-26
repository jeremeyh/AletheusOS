"""Planner engine for RUF012 repository maintenance."""

from __future__ import annotations

from tools.maintenance.ruf012.extractor import (
    CandidateClassification,
    ExtractedCandidate,
    ExtractionFailure,
)
from tools.maintenance.ruf012.planner.models import (
    PlannedRewrite,
    PlannerSummary,
    PlanStatus,
)


class PlannerEngine:
    """Build rewrite plans from extracted candidates."""

    def build_plan(
        self,
        candidates: tuple[ExtractedCandidate, ...],
        failures: tuple[ExtractionFailure, ...] = (),
    ) -> PlannerSummary:
        """Build a repository rewrite plan."""

        rewrites: list[PlannedRewrite] = []

        for candidate in candidates:
            rewrites.append(self._candidate_to_plan(candidate))

        for failure in failures:
            rewrites.append(
                PlannedRewrite(
                    path=failure.path,
                    class_name="<unknown>",
                    attribute_name="<unknown>",
                    line_number=failure.line_number or 0,
                    status=PlanStatus.FAILED,
                    reason=failure.error,
                )
            )

        return PlannerSummary(rewrites=tuple(rewrites))

    def _candidate_to_plan(
        self,
        candidate: ExtractedCandidate,
    ) -> PlannedRewrite:
        """Convert one extracted candidate into a planned rewrite."""

        if candidate.classification is CandidateClassification.SAFE:
            status = PlanStatus.READY
            reason = ""
        else:
            status = PlanStatus.SKIPPED
            reason = candidate.reason

        return PlannedRewrite(
            path=candidate.path,
            class_name=candidate.class_name,
            attribute_name=candidate.attribute_name,
            line_number=candidate.line_number,
            status=status,
            reason=reason,
        )
