"""Tests for unified diff generation."""

from __future__ import annotations

from pathlib import Path

from tools.maintenance.ruf012.diff import create_unified_diff


def test_create_unified_diff_uses_git_style_paths() -> None:
    result = create_unified_diff(
        path=Path("package/example.py"),
        original_source="VALUE = []\n",
        rewritten_source="VALUE: ClassVar = []\n",
    )

    assert "--- a/package/example.py" in result
    assert "+++ b/package/example.py" in result
    assert "-VALUE = []" in result
    assert "+VALUE: ClassVar = []" in result
