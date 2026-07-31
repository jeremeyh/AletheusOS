"""Evolution plan validation and operation preview."""

from __future__ import annotations

from pathlib import Path

from .errors import PlanValidationError, PreconditionsFailed
from .hashing import sha256_file
from .models import EvolutionPlan, Operation
from .paths import resolve_inside


def _validate_operation(root: Path, operation: Operation) -> None:
    source = resolve_inside(root, operation.path)

    if operation.operation == "replace_text":
        if not source.is_file():
            raise PlanValidationError(
                f"replace_text source does not exist: {operation.path}"
            )
        if operation.old is None or operation.new is None:
            raise PlanValidationError("replace_text requires old and new strings.")
        text = source.read_text(encoding="utf-8")
        if operation.old not in text:
            raise PreconditionsFailed(
                f"replace_text old value not found in {operation.path}"
            )

    elif operation.operation == "write_file":
        if operation.content is None:
            raise PlanValidationError("write_file requires content.")

    elif operation.operation == "move_file":
        if not source.is_file():
            raise PlanValidationError(
                f"move_file source does not exist: {operation.path}"
            )
        if not operation.destination:
            raise PlanValidationError("move_file requires destination.")
        destination = resolve_inside(root, operation.destination)
        if destination.exists():
            raise PreconditionsFailed(
                f"move_file destination already exists: {operation.destination}"
            )

    if operation.expected_sha256 is not None:
        if not source.is_file():
            raise PreconditionsFailed(
                f"Hash precondition requires an existing file: {operation.path}"
            )
        actual = sha256_file(source)
        if actual != operation.expected_sha256:
            raise PreconditionsFailed(
                f"SHA-256 mismatch for {operation.path}: expected "
                f"{operation.expected_sha256}, got {actual}"
            )


def validate_plan(root: Path, plan: EvolutionPlan) -> None:
    seen: set[str] = set()
    for operation in plan.operations:
        if operation.path in seen:
            raise PlanValidationError(
                f"Multiple operations target the same path: {operation.path}"
            )
        seen.add(operation.path)
        _validate_operation(root, operation)
