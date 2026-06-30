from aletheus.runtime import runtime_core


def test_agent_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Autonomous Agent Runtime" in diagnostics["services"]


def test_agent_bootstrap():
    result = runtime_core.commands.dispatch("agent.bootstrap", {})
    assert not result.errors, result.errors
    assert result.results["agents"]["agents"] >= 5


def test_spawn_assign_message_pause_resume_stop():
    spawned = runtime_core.commands.dispatch(
        "agent.spawn",
        {"name": "Test Agent", "role": "Testing"},
    )
    assert not spawned.errors, spawned.errors

    agent = spawned.results["agent"]
    agent_id = agent["agent_id"]

    assigned = runtime_core.commands.dispatch(
        "agent.assign",
        {"agent_id": agent_id, "mission": "Validate v2.7 autonomous agent runtime."},
    )
    assert not assigned.errors, assigned.errors
    assert assigned.results["agent"]["status"] == "working"

    message = runtime_core.commands.dispatch(
        "agent.message",
        {
            "sender": "Founder",
            "recipient": "Test Agent",
            "message": "Proceed with validation.",
        },
    )
    assert not message.errors, message.errors
    assert message.results["message"]["messages"] >= 1

    paused = runtime_core.commands.dispatch("agent.pause", {"agent_id": agent_id})
    assert not paused.errors, paused.errors
    assert paused.results["agent"]["status"] == "paused"

    resumed = runtime_core.commands.dispatch("agent.resume", {"agent_id": agent_id})
    assert not resumed.errors, resumed.errors
    assert resumed.results["agent"]["status"] == "working"

    stopped = runtime_core.commands.dispatch("agent.stop", {"agent_id": agent_id})
    assert not stopped.errors, stopped.errors
    assert stopped.results["agent"]["status"] == "stopped"


def test_agent_heartbeat_and_stats():
    heartbeat = runtime_core.commands.dispatch("agent.heartbeat", {})
    assert not heartbeat.errors, heartbeat.errors
    assert "heartbeat" in heartbeat.results

    stats = runtime_core.commands.dispatch("agent.statistics", {})
    assert not stats.errors, stats.errors
    assert "agent_stats" in stats.results


if __name__ == "__main__":
    test_agent_service_registered()
    test_agent_bootstrap()
    test_spawn_assign_message_pause_resume_stop()
    test_agent_heartbeat_and_stats()
    print("Aletheus v2.7 Autonomous Agent Runtime tests passed.")
