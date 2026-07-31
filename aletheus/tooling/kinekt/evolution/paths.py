"""Repository path safety."""

from __future__ import annotations

from pathlib import Path

from .errors import PlanValidationError


def resolve_inside(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise PlanValidationError(
            f"Path escapes repository boundary: {relative}"
        ) from exc
    return candidate
