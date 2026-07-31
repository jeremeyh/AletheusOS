"""Load and validate evolution plan documents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .errors import PlanValidationError
from .models import EvolutionPlan, Operation, ValidationSpec

_ALLOWED_OPERATIONS = {"replace_text", "write_file", "move_file"}


def _string_tuple(value: Any, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise PlanValidationError(f"{field} must be a list of strings.")
    return tuple(value)


def load_plan(path: Path) -> EvolutionPlan:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise PlanValidationError("Evolution plan root must be an object.")

    plan_id = payload.get("plan_id")
    summary = payload.get("summary")
    raw_operations = payload.get("operations")

    if not isinstance(plan_id, str) or not plan_id.strip():
        raise PlanValidationError("plan_id must be a non-empty string.")
    if not isinstance(summary, str) or not summary.strip():
        raise PlanValidationError("summary must be a non-empty string.")
    if not isinstance(raw_operations, list) or not raw_operations:
        raise PlanValidationError("operations must be a non-empty list.")

    operations: list[Operation] = []
    for index, raw in enumerate(raw_operations):
        if not isinstance(raw, dict):
            raise PlanValidationError(f"operations[{index}] must be an object.")

        operation = raw.get("operation")
        path_value = raw.get("path")
        if operation not in _ALLOWED_OPERATIONS:
            raise PlanValidationError(
                f"operations[{index}].operation is unsupported: {operation!r}"
            )
        if not isinstance(path_value, str) or not path_value.strip():
            raise PlanValidationError(f"operations[{index}].path is required.")

        operations.append(
            Operation(
                operation=operation,
                path=path_value,
                expected_sha256=raw.get("expected_sha256"),
                old=raw.get("old"),
                new=raw.get("new"),
                content=raw.get("content"),
                destination=raw.get("destination"),
            )
        )

    raw_validation = payload.get("validation", {})
    if not isinstance(raw_validation, dict):
        raise PlanValidationError("validation must be an object.")

    validation = ValidationSpec(
        ruff_targets=_string_tuple(
            raw_validation.get("ruff_targets"), "validation.ruff_targets"
        ),
        compile_targets=_string_tuple(
            raw_validation.get("compile_targets"), "validation.compile_targets"
        ),
        pytest_targets=_string_tuple(
            raw_validation.get("pytest_targets"), "validation.pytest_targets"
        ),
    )

    return EvolutionPlan(
        plan_id=plan_id,
        summary=summary,
        operations=tuple(operations),
        validation=validation,
    )
