import json

from aletheus.tooling.end_to_end_path_resolver.engine import Engine


def test_path_resolver_finds_roots_and_leaves(tmp_path) -> None:
    wiring = tmp_path / "wiring.json"
    wiring.write_text(json.dumps({"routes": [{"source": "A", "target": "B"}]}))
    result = Engine(wiring, tmp_path / "out").build()
    assert result["roots"] == ["A"]
    assert result["leaves"] == ["B"]
