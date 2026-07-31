from aletheus.tooling.kinekt.dependency.builder import build_dependency_graph


def test_dependency_graph_builds_semantic_nodes() -> None:
    repository = {
        "modules": [
            {
                "module": "aletheus.runtime.core",
                "package": "aletheus.runtime",
                "owner": "Constitutional Runtime Kernel",
                "path": "aletheus/runtime/core.py",
            },
            {
                "module": "aletheus.cardhawk.app",
                "package": "aletheus.cardhawk",
                "owner": "Product Application",
                "path": "aletheus/cardhawk/app.py",
            },
        ]
    }
    topology = {
        "modules": [
            {
                "module": "aletheus.runtime.core",
                "outgoing": ["aletheus.cardhawk.app"],
            },
            {
                "module": "aletheus.cardhawk.app",
                "outgoing": [],
            },
        ]
    }

    nodes, relationships, findings, unresolved = build_dependency_graph(
        repository,
        topology,
    )

    assert any(node.node_id == "runtime:crk" for node in nodes)
    assert any(item.relationship == "imports" for item in relationships)
    assert len(findings) == 1
    assert unresolved == []
