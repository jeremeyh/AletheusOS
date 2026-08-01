from aletheus.tooling.kinekt.authority.analysis import assign_modules, parse_authorities


def test_assignment():
    a = parse_authorities(
        {
            "capabilities": [
                {
                    "name": "Kinekt",
                    "runtime_role": "architectural_intelligence",
                    "module_prefixes": ["aletheus.tooling.kinekt"],
                }
            ]
        }
    )
    assignments, unresolved, findings = assign_modules(
        {"nodes": [{"node_type": "module", "name": "aletheus.tooling.kinekt.engine"}]},
        a,
    )
    assert assignments["aletheus.tooling.kinekt.engine"] == "Kinekt"
    assert not unresolved
    assert not findings
