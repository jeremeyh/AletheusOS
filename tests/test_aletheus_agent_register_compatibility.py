from aletheus.runtime import runtime_core


def test_agent_register_preserves_legacy_contract():
    payload = {
        "name": "Agent Registration Compatibility Test",
        "role": "compatibility",
        "description": "Verifies the historical agent.register runtime contract.",
        "capabilities": [
            {
                "name": "contract_probe",
                "description": "Verifies compatibility metadata preservation.",
            }
        ],
    }

    first = runtime_core.commands.dispatch("agent.register", payload)

    assert first.errors == []

    first_agent = first.results["agent"]

    assert first_agent["name"] == payload["name"]
    assert first_agent["role"] == payload["role"]
    assert first_agent["description"] == payload["description"]
    assert first_agent["capabilities"] == payload["capabilities"]

    second = runtime_core.commands.dispatch("agent.register", payload)

    assert second.errors == []

    second_agent = second.results["agent"]

    assert second_agent["agent_id"] == first_agent["agent_id"]
