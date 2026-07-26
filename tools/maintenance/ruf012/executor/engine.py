"""Execution engine for RUF012 preview planning."""

from __future__ import annotations

from tools.maintenance.ruf012.executor.models import (
    ExecutionResult,
    ExecutionStatus,
    ExecutionSummary,
)
from tools.maintenance.ruf012.planner import (
    PlannedRewrite,
    PlanStatus,
)


class ExecutionEngine:
    """Converts rewrite plans into execution results."""

    def execute(
        self,
        rewrites: tuple[PlannedRewrite, ...],
    ) -> ExecutionSummary:
        """Execute a preview plan."""

        results: list[ExecutionResult] = []

        for rewrite in rewrites:
            results.append(self._execute_one(rewrite))

        return ExecutionSummary(results=tuple(results))

    def _execute_one(
        self,
        rewrite: PlannedRewrite,
    ) -> ExecutionResult:
        """Execute one planned rewrite."""

        if rewrite.status is PlanStatus.SKIPPED:
            return ExecutionResult(
                path=rewrite.path,
                candidate_name=rewrite.candidate_name,
                status=ExecutionStatus.SKIPPED,
                message=rewrite.reason,
                validated=False,
            )

        if rewrite.status is PlanStatus.FAILED:
            return ExecutionResult(
                path=rewrite.path,
                candidate_name=rewrite.candidate_name,
                status=ExecutionStatus.FAILED,
                message=rewrite.reason,
                validated=False,
            )

        return ExecutionResult(
            path=rewrite.path,
            candidate_name=rewrite.candidate_name,
            status=ExecutionStatus.PREVIEWED,
            message="Preview execution scheduled.",
            validated=True,
        )
