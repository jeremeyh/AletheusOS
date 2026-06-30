from aletheus.runtime import runtime_core


def test_knowledge_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Knowledge Graph Engine" in diagnostics["services"]


def test_entity_create_and_search():
    created = runtime_core.commands.dispatch(
        "entity.create",
        {
            "label": "Caleb Williams",
            "entity_type": "player",
            "properties": {"team": "Chicago Bears"},
        },
    )

    assert not created.errors
    entity = created.results["entity"]
    assert entity["label"] == "Caleb Williams"

    searched = runtime_core.commands.dispatch(
        "entity.search",
        {"label": "Caleb", "entity_type": "player"},
    )

    assert not searched.errors
    assert len(searched.results["entities"]) >= 1


def test_relationship_create_and_graph_query():
    source = runtime_core.commands.dispatch(
        "entity.create",
        {"label": "Card Hawk Foundation", "entity_type": "application"},
    ).results["entity"]

    target = runtime_core.commands.dispatch(
        "entity.create",
        {"label": "Aletheus", "entity_type": "operating_system"},
    ).results["entity"]

    rel = runtime_core.commands.dispatch(
        "relationship.create",
        {
            "source_id": source["entity_id"],
            "target_id": target["entity_id"],
            "relationship_type": "runs_on",
        },
    )

    assert not rel.errors
    assert rel.results["relationship"]["relationship_type"] == "runs_on"

    graph = runtime_core.commands.dispatch(
        "graph.query",
        {"entity_id": source["entity_id"]},
    )

    assert not graph.errors
    assert len(graph.results["graph_query"]["outgoing"]) >= 1


def test_graph_stats():
    stats = runtime_core.commands.dispatch("graph.stats", {})
    assert not stats.errors
    assert stats.results["graph_stats"]["entities"] >= 1


if __name__ == "__main__":
    test_knowledge_service_registered()
    test_entity_create_and_search()
    test_relationship_create_and_graph_query()
    test_graph_stats()
    print("Aletheus Genesis 0.6 Knowledge Graph Engine tests passed.")
