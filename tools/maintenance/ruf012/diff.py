"""Unified diff generation."""

from __future__ import annotations

import difflib
from pathlib import Path


def create_unified_diff(
    *, path: Path, original_source: str, rewritten_source: str
) -> str:
    relative_path = path.as_posix()
    return "".join(
        difflib.unified_diff(
            original_source.splitlines(keepends=True),
            rewritten_source.splitlines(keepends=True),
            fromfile=f"a/{relative_path}",
            tofile=f"b/{relative_path}",
        )
    )
