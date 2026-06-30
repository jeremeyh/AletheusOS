from aletheus.runtime import runtime_core


def test_agent_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Multi-Agent Orchestration Layer" in diagnostics["services"]


def test_default_agents_bootstrapped():
    result = runtime_core.commands.dispatch("agent.bootstrap", {})
    assert not result.errors
    assert len(result.results["agents"]) >= 6


def test_assign_and_run_agent_task():
    assigned = runtime_core.commands.dispatch(
        "agent.task.assign",
        {
            "agent_name": "Executive Agent",
            "title": "Review current system state",
            "payload": {"test": True},
        },
    )
    assert not assigned.errors
    assert "task" in assigned.results

    run = runtime_core.commands.dispatch(
        "agent.run",
        {"agent_name": "Executive Agent"},
    )
    assert not run.errors
    assert "agent_run" in run.results


def test_orchestrate_objective():
    result = runtime_core.commands.dispatch(
        "agent.orchestrate",
        {"objective": "Validate multi-agent orchestration."},
    )
    assert not result.errors
    assert "orchestration" in result.results
    assert len(result.results["orchestration"]["results"]) >= 1


if __name__ == "__main__":
    test_agent_service_registered()
    test_default_agents_bootstrapped()
    test_assign_and_run_agent_task()
    test_orchestrate_objective()
    print("Aletheus v1.3 Multi-Agent Orchestration tests passed.")
