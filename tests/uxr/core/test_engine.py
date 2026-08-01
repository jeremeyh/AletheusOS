from pathlib import Path

from aletheus.uxr.core.engine import Engine
from aletheus.uxr.core.models import Experience, Node, RuntimeMeta


def test_x(tmp_path: Path):
    e = Experience(
        "23.0.0",
        RuntimeMeta("T", "summary", {}),
        Node("LayoutContainer", {}),
        "e",
        "1.0.0",
    )
    assert "constitutionalSignature" in Engine().finalize(e, tmp_path)
