from pathlib import Path

from aletheus.span.constitutional_compliance.engine import Engine


def test_constitutional_compliance(tmp_path: Path) -> None:
    (tmp_path / "sample.py").write_text("VALUE = 1\n")
    result = Engine().analyze(tmp_path)
    assert result["humanAuthority"] == "PRESERVED"
    assert result["executionAuthorized"] is False
    assert result["digest"]
