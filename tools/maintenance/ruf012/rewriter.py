"""Read-only candidate transformation orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .diff import create_unified_diff
from .models import RewritePreview
from .registry import TransformationRegistry
from .transforms import TransformationError
from .utils.candidates import candidate_path
from .validator import SourceValidator


class RewriteError(RuntimeError):
    pass


class CandidateRewriter:
    def __init__(
        self,
        root: Path,
        *,
        registry: TransformationRegistry | None = None,
        validator: SourceValidator | None = None,
    ) -> None:
        self.root = Path(root).resolve()
        self.registry = registry or TransformationRegistry()
        self.validator = validator or SourceValidator()

    def preview(self, candidate: Any) -> RewritePreview:
        transformation = self.registry.resolve(candidate)
        if transformation is None:
            classification = getattr(candidate, "classification", None)
            raise RewriteError(
                "No registered transformation supports candidate "
                f"classification {classification!r}."
            )
        path = self._resolve_candidate_path(candidate)
        original_source = path.read_text(encoding="utf-8")
        try:
            rewritten_source, notes = transformation.transform(
                candidate=candidate,
                path=path,
                source=original_source,
            )
        except TransformationError as exc:
            raise RewriteError(str(exc)) from exc
        validation = self.validator.validate(rewritten_source, path)
        if not validation.valid:
            raise RewriteError(
                f"Rewritten source failed validation: {validation.error}"
            )
        if rewritten_source == original_source:
            raise RewriteError("Transformation completed without changing source.")
        relative_path = path.relative_to(self.root)
        diff = create_unified_diff(
            path=relative_path,
            original_source=original_source,
            rewritten_source=rewritten_source,
        )
        if not diff:
            raise RewriteError("Transformation changed source but produced no diff.")
        return RewritePreview(
            candidate=candidate,
            path=path,
            original_source=original_source,
            rewritten_source=rewritten_source,
            diff=diff,
            changed=True,
            validated=True,
            transformation=transformation.name,
            notes=notes,
        )

    def _resolve_candidate_path(self, candidate: Any) -> Path:
        raw_path = candidate_path(candidate)
        resolved = (
            raw_path.resolve()
            if raw_path.is_absolute()
            else (self.root / raw_path).resolve()
        )
        try:
            resolved.relative_to(self.root)
        except ValueError as exc:
            raise RewriteError(
                f"Candidate path escapes repository root: {resolved}"
            ) from exc
        if not resolved.is_file():
            raise RewriteError(f"Candidate file does not exist: {resolved}")
        return resolved
