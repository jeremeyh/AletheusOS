import json

from aletheus.tooling.runtime_explorer.engine import RuntimeExplorer


def test_impact_navigation(tmp_path) -> None:
    twin = tmp_path / "twin.json"
    twin.write_text(
        json.dumps(
            {
                "nodes": [
                    {"node_id": "a"},
                    {"node_id": "b"},
                    {"node_id": "c"},
                ],
                "relationships": [
                    {"source": "a", "target": "b"},
                    {"source": "b", "target": "c"},
                ],
            }
        )
    )
    explorer = RuntimeExplorer(twin)
    result = explorer.impact("b", depth=1)
    assert result["upstream"] == ["a"]
    assert result["downstream"] == ["c"]
