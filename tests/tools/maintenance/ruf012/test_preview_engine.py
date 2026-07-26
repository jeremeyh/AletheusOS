from pathlib import Path
from typing import Any

import pytest

from tools.maintenance.ruf012.diff import create_unified_diff
from tools.maintenance.ruf012.rewriter import CandidateRewriter, RewriteError
from tools.maintenance.ruf012.transforms import ClassVarTransformation
from tools.maintenance.ruf012.validator import SourceValidator


def test_validator_accepts_valid_python() -> None:
    result = SourceValidator().validate("class Example:\n    VALUES = []\n", Path("example.py"))
    assert result.valid is True
    assert result.error is None

def test_diff_uses_git_style_paths() -> None:
    result = create_unified_diff(
        path=Path("package/example.py"),
        original_source="VALUE = []\n",
        rewritten_source="VALUE: ClassVar = []\n",
    )
    assert "--- a/package/example.py" in result
    assert "+++ b/package/example.py" in result

def test_classvar_transformation(candidate_factory: Any) -> None:
    rewritten, _ = ClassVarTransformation().transform(
        candidate=candidate_factory(),
        path=Path("sample.py"),
        source="class Example:\n    VALUES = []\n",
    )
    assert "from typing import ClassVar\n" in rewritten
    assert "    VALUES: ClassVar = []\n" in rewritten

def test_preview_is_read_only(tmp_path: Path, candidate_factory: Any) -> None:
    source_path = tmp_path / "sample.py"
    original_source = "class Example:\n    VALUES = []\n"
    source_path.write_text(original_source, encoding="utf-8")
    preview = CandidateRewriter(tmp_path).preview(candidate_factory())
    assert preview.changed is True
    assert preview.validated is True
    assert source_path.read_text(encoding="utf-8") == original_source

def test_unsupported_candidate(tmp_path: Path, candidate_factory: Any) -> None:
    source_path = tmp_path / "sample.py"
    source_path.write_text("class Example:\n    VALUES = []\n", encoding="utf-8")
    with pytest.raises(RewriteError, match="No registered transformation supports"):
        CandidateRewriter(tmp_path).preview(
            candidate_factory(classification="manual-review")
        )
