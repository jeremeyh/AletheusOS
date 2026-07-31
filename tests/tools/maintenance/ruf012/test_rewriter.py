"""Tests for CandidateRewriter orchestration."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from tools.maintenance.ruf012.rewriter import (
    CandidateRewriter,
    RewriteError,
)


def test_preview_generates_validated_diff(
    tmp_path: Path,
    candidate_factory: Any,
) -> None:
    source_path = tmp_path / "sample.py"
    source_path.write_text(
        "class Example:\n    VALUES = []\n",
        encoding="utf-8",
    )
    candidate = candidate_factory(line=2)

    preview = CandidateRewriter(tmp_path).preview(candidate)

    assert preview.changed is True
    assert preview.validated is True
    assert preview.transformation == "ruf012-classvar"
    assert "-    VALUES = []" in preview.diff
    assert "+    VALUES: ClassVar = []" in preview.diff
    assert "from typing import ClassVar" in preview.rewritten_source

    ast.parse(preview.rewritten_source)


def test_preview_does_not_modify_source_file(
    tmp_path: Path,
    candidate_factory: Any,
) -> None:
    source_path = tmp_path / "sample.py"
    original_source = "class Example:\n    VALUES = []\n"
    source_path.write_text(original_source, encoding="utf-8")
    candidate = candidate_factory(line=2)

    CandidateRewriter(tmp_path).preview(candidate)

    assert source_path.read_text(encoding="utf-8") == original_source


def test_preview_rejects_unsupported_classification(
    tmp_path: Path,
    candidate_factory: Any,
) -> None:
    source_path = tmp_path / "sample.py"
    source_path.write_text(
        "class Example:\n    VALUES = []\n",
        encoding="utf-8",
    )
    candidate = candidate_factory(
        line=2,
        classification="manual-review",
    )

    with pytest.raises(
        RewriteError,
        match="No registered transformation supports",
    ):
        CandidateRewriter(tmp_path).preview(candidate)


def test_preview_rejects_missing_file(
    tmp_path: Path,
    candidate_factory: Any,
) -> None:
    candidate = candidate_factory(path="missing.py", line=2)

    with pytest.raises(
        RewriteError,
        match="Candidate file does not exist",
    ):
        CandidateRewriter(tmp_path).preview(candidate)


def test_preview_rejects_repository_escape(
    tmp_path: Path,
    candidate_factory: Any,
) -> None:
    candidate = candidate_factory(
        path="../outside.py",
        line=2,
    )

    with pytest.raises(
        RewriteError,
        match="escapes repository root",
    ):
        CandidateRewriter(tmp_path).preview(candidate)
