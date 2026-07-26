"""Validation for transformed Python source."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    error: str | None = None

class SourceValidator:
    def validate(self, source: str, path: Path) -> ValidationResult:
        try:
            ast.parse(source, filename=str(path))
            compile(source, str(path), "exec")
        except (SyntaxError, TypeError, ValueError) as exc:
            return ValidationResult(valid=False, error=str(exc))
        return ValidationResult(valid=True)
