from aletheus.tooling.kinekt.cohesion.analysis import analyze_packages


def test_fragmented_package_is_flagged() -> None:
    topology = {
        "packages": [
            {
                "package": "aletheus.fragmented",
                "modules": 10,
                "internal_edges": 0,
                "inbound_packages": [],
                "outbound_packages": [
                    "a",
                    "b",
                    "c",
                    "d",
                    "e",
                    "f",
                    "g",
                    "h",
                ],
                "cycle_groups": 1,
                "isolated_modules": 9,
            }
        ]
    }
    dependency = {"nodes": []}

    result = analyze_packages(topology, dependency)

    assert result[0].status in {"fragmented", "critical"}
    assert result[0].recommendations
