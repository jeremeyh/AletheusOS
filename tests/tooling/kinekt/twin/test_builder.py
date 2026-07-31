from aletheus.tooling.kinekt.twin.builder import build_nodes


def test_build_nodes_merges_repository_and_dependency_data() -> None:
    repository = {
        "modules": [
            {
                "module": "aletheus.runtime.core",
                "package": "aletheus.runtime",
                "path": "aletheus/runtime/core.py",
            }
        ]
    }
    dependency = {
        "nodes": [
            {
                "node_id": "module:aletheus.runtime.core",
                "node_type": "module",
                "name": "aletheus.runtime.core",
                "capability": "Constitutional Runtime Kernel",
            }
        ]
    }

    nodes = build_nodes(repository, dependency)

    assert len(nodes) == 1
    assert nodes[0].attributes["capability"] == "Constitutional Runtime Kernel"
