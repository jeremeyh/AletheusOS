from aletheus.runtime import runtime_core


def test_telemetry_service_registered():

    ctx = runtime_core.commands.dispatch("runtime.diagnostics")

    diagnostics = ctx.results["diagnostics"]

    assert "Aletheus Observability Platform" in diagnostics["services"]


def test_bootstrap():

    result = runtime_core.commands.dispatch(
        "telemetry.bootstrap",
        {},
    )

    assert not result.errors, result.errors

    stats = result.results["telemetry"]

    assert stats["health"] == "healthy"


def test_metric():

    result = runtime_core.commands.dispatch(

        "telemetry.metric",

        {
            "name": "runtime.commands",

            "value": 250,

            "category": "runtime",
        },
    )

    assert not result.errors

    metric = result.results["metric"]

    assert metric["name"] == "runtime.commands"

    assert metric["value"] == 250


def test_record():

    result = runtime_core.commands.dispatch(

        "telemetry.record",

        {
            "name": "runtime.memory",

            "value": 512,
        },
    )

    assert not result.errors


def test_log():

    result = runtime_core.commands.dispatch(

        "telemetry.log",

        {
            "level": "INFO",

            "message": "Telemetry operational",

            "source": "unit-test",
        },
    )

    assert not result.errors

    log = result.results["log"]

    assert log["level"] == "INFO"


def test_trace():

    result = runtime_core.commands.dispatch(

        "telemetry.trace",

        {
            "name": "workflow.execute",

            "status": "completed",
        },
    )

    assert not result.errors

    trace = result.results["trace"]

    assert trace["status"] == "completed"


def test_health():

    result = runtime_core.commands.dispatch(

        "telemetry.health",

        {
            "component": "workflow",

            "status": "healthy",
        },
    )

    assert not result.errors

    health = result.results["health"]

    assert health["status"] == "healthy"


def test_timeline():

    result = runtime_core.commands.dispatch(

        "telemetry.timeline",

        {
            "message": "Workflow executed",

            "source": "workflow",
        },
    )

    assert not result.errors

    timeline = result.results["timeline"]

    assert timeline["message"] == "Workflow executed"


def test_statistics():

    result = runtime_core.commands.dispatch(

        "telemetry.statistics",

        {},
    )

    assert not result.errors

    stats = result.results["telemetry_stats"]

    assert stats["health"] == "healthy"


if __name__ == "__main__":

    test_telemetry_service_registered()
    test_bootstrap()
    test_metric()
    test_record()
    test_log()
    test_trace()
    test_health()
    test_timeline()
    test_statistics()

    print("\n✔ AletheusOS v3.5 Observability Platform tests passed.")
