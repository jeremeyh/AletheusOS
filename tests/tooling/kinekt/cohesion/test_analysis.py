from aletheus.tooling.kinekt.cohesion.analysis import analyze_packages


def test_cohesive_package_scores_higher() -> None:
    topology = {
        "packages": [
            {
                "package": "aletheus.alpha",
                "modules": 4,
                "internal_edges": 6,
                "inbound_packages": [],
                "outbound_packages": ["aletheus.beta"],
                "cycle_groups": 0,
                "isolated_modules": 0,
            }
        ]
    }
    dependency = {
        "nodes": [
            {
                "node_id": "module:aletheus.alpha.one",
                "node_type": "module",
                "name": "aletheus.alpha.one",
                "owner": "Alpha",
                "capability": "Alpha",
                "evidence": ["aletheus/alpha/one.py"],
            }
        ]
    }

    result = analyze_packages(topology, dependency)

    assert result[0].score >= 90
