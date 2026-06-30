from aletheus.runtime import runtime_core


def test_knowledge_graph_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Knowledge Graph Engine" in diagnostics["services"]


def test_entity_and_relationship_creation():
    source = runtime_core.commands.dispatch(
        "knowledge.entity.create",
        {
            "name": "Card Hawk Foundation Test",
            "node_type": "application",
            "properties": {"domain": "collectibles"},
        },
    )
    target = runtime_core.commands.dispatch(
        "knowledge.entity.create",
        {
            "name": "Asset Vault Test",
            "node_type": "service",
            "properties": {"category": "assets"},
        },
    )

    assert not source.errors, source.errors
    assert not target.errors, target.errors

    rel = runtime_core.commands.dispatch(
        "knowledge.relationship.create",
        {
            "source_id": source.results["entity"]["node_id"],
            "target_id": target.results["entity"]["node_id"],
            "relationship_type": "owns",
        },
    )

    assert not rel.errors, rel.errors
    assert rel.results["relationship"]["relationship_type"] == "owns"


def test_neighbors_and_search():
    search = runtime_core.commands.dispatch(
        "knowledge.search",
        {"query": "Card Hawk"},
    )
    assert not search.errors, search.errors
    assert len(search.results["results"]) >= 1

    node = search.results["results"][0]

    neighbors = runtime_core.commands.dispatch(
        "knowledge.neighbors",
        {"node_id": node["node_id"]},
    )

    assert not neighbors.errors, neighbors.errors
    assert "neighbors" in neighbors.results


def test_bootstrap_and_inference():
    boot = runtime_core.commands.dispatch("knowledge.bootstrap.cardhawk", {})
    assert not boot.errors, boot.errors
    assert "graph" in boot.results
    assert len(boot.results["graph"]["nodes"]) >= 1
    assert len(boot.results["graph"]["relationships"]) >= 1

    inferred = runtime_core.commands.dispatch("knowledge.infer", {})
    assert not inferred.errors, inferred.errors
    assert "inference" in inferred.results


def test_graph_stats():
    result = runtime_core.commands.dispatch("knowledge.statistics", {})
    assert not result.errors, result.errors
    assert "knowledge_graph_stats" in result.results


if __name__ == "__main__":
    test_knowledge_graph_service_registered()
    test_entity_and_relationship_creation()
    test_neighbors_and_search()
    test_bootstrap_and_inference()
    test_graph_stats()
    print("Aletheus v2.4 Knowledge Graph Engine tests passed.")
