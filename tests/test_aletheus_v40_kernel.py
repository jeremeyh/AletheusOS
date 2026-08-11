from aletheus.runtime import runtime_core


def test_kernel_bootstrap():

    ctx = runtime_core.commands.dispatch(
        "kernel.bootstrap",
        {},
    )

    assert not ctx.errors, ctx.errors

    kernel = ctx.results["kernel"]

    assert kernel["health"] == "healthy"


def test_kernel_execute():

    ctx = runtime_core.commands.dispatch(
        "kernel.execute",
        {
            "command": "runtime.diagnostics",
            "payload": {},
        },
    )

    assert not ctx.errors, ctx.errors

    task = ctx.results["task"]

    assert task["status"] == "completed"

    assert "diagnostics" in task["result"]


def test_kernel_task_history():

    ctx = runtime_core.commands.dispatch(
        "kernel.tasks",
        {},
    )

    assert not ctx.errors

    tasks = ctx.results["tasks"]["tasks"]

    assert len(tasks) >= 1


def test_kernel_scheduler():

    task = runtime_core.intelligence_orchestrator.create_task(
        command="runtime.diagnostics",
        payload={},
    )

    ctx = runtime_core.commands.dispatch(
        "kernel.scheduler",
        {
            "task_id": task["task_id"],
            "priority": 3,
        },
    )

    assert not ctx.errors

    schedule = ctx.results["schedule"]

    assert schedule["priority"] == 3


def test_kernel_dispatcher():

    ctx = runtime_core.commands.dispatch(
        "kernel.dispatcher",
        {
            "command": "runtime.diagnostics",
            "payload": {},
        },
    )

    assert not ctx.errors

    dispatch = ctx.results["dispatch"]

    assert dispatch["errors"] == []

    assert "diagnostics" in dispatch["results"]


def test_kernel_supervisor():

    ctx = runtime_core.commands.dispatch(
        "kernel.supervisor",
        {},
    )

    assert not ctx.errors

    supervisor = ctx.results["supervisor"]

    assert supervisor["health"] == "healthy"


def test_kernel_statistics():

    ctx = runtime_core.commands.dispatch(
        "kernel.statistics",
        {},
    )

    assert not ctx.errors

    stats = ctx.results["kernel_stats"]

    assert stats["orchestrator"]["health"] == "healthy"

    assert stats["scheduler"]["health"] == "healthy"

    assert stats["dispatcher"]["health"] == "healthy"

    assert stats["supervisor"]["health"] == "healthy"


def test_kernel_executor():

    result = runtime_core.kernel.execute(
        "runtime.diagnostics",
        {},
    )

    assert result["status"] == "completed"

    assert result["errors"] == []

    assert "diagnostics" in result["result"]


def test_kernel_multiple_execution():

    before = runtime_core.intelligence_orchestrator.statistics()["tasks"]

    runtime_core.kernel.execute(
        "runtime.diagnostics",
        {},
    )

    runtime_core.kernel.execute(
        "tenant.health",
        {},
    )

    after = runtime_core.intelligence_orchestrator.statistics()["tasks"]

    assert after >= before + 2


if __name__ == "__main__":
    test_kernel_bootstrap()
    test_kernel_execute()
    test_kernel_task_history()
    test_kernel_scheduler()
    test_kernel_dispatcher()
    test_kernel_supervisor()
    test_kernel_statistics()
    test_kernel_executor()
    test_kernel_multiple_execution()

    print("\n✔ AletheusOS v4.0 Intelligence Kernel tests passed.")
