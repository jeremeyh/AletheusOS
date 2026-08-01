import json

from aletheus.tooling.runtime_knowledge_graph.engine import KnowledgeGraphEngine


def test_graph_build(tmp_path) -> None:
    registry = tmp_path / "registry.json"
    twin = tmp_path / "twin.json"
    registry.write_text(json.dumps({"capabilities": []}))
    twin.write_text(
        json.dumps(
            {
                "nodes": [{"node_id": "a"}, {"node_id": "b"}],
                "relationships": [{"source": "a", "target": "b"}],
            }
        )
    )
    graph = KnowledgeGraphEngine(registry, twin, tmp_path / "out").build()
    assert graph["adjacency"]["a"] == ["b"]
