"""Read-only transformation transaction boundary."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import RewritePreview


@dataclass(frozen=True)
class TransactionResult:
    path: Path
    committed: bool
    message: str

class DryRunTransaction:
    def apply(self, preview: RewritePreview) -> TransactionResult:
        if not preview.validated:
            return TransactionResult(preview.path, False, "Preview was not validated.")
        if not preview.changed:
            return TransactionResult(preview.path, False, "Preview contains no source change.")
        return TransactionResult(
            preview.path,
            False,
            "Dry run complete; no source file was modified.",
        )
