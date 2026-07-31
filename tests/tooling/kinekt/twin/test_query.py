import json

from aletheus.tooling.kinekt.twin.query import query_node


def test_query_node(tmp_path) -> None:
    snapshot = tmp_path / "snapshot.json"
    snapshot.write_text(
        json.dumps(
            {
                "nodes": [
                    {
                        "node_id": "module:example",
                        "name": "example",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = query_node(snapshot, "module:example")

    assert result is not None
    assert result["name"] == "example"
