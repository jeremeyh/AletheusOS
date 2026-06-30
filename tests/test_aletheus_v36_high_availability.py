from aletheus.runtime import runtime_core


def test_ha_service_registered():

    ctx = runtime_core.commands.dispatch("runtime.diagnostics")

    diagnostics = ctx.results["diagnostics"]

    assert "Aletheus High Availability Platform" in diagnostics["services"]


def test_bootstrap():

    result = runtime_core.commands.dispatch(
        "ha.bootstrap",
        {},
    )

    assert not result.errors, result.errors

    stats = result.results["ha"]

    assert stats["health"] == "healthy"

    assert stats["nodes"] >= 1


def test_join():

    result = runtime_core.commands.dispatch(

        "ha.join",

        {
            "name": "Replica Runtime",
        },
    )

    assert not result.errors

    node = result.results["node"]

    assert node["name"] == "Replica Runtime"

    return node["node_id"]


def test_status():

    result = runtime_core.commands.dispatch(
        "ha.status",
        {},
    )

    assert not result.errors

    status = result.results["ha_status"]

    assert status["leader"] is not None

    assert len(status["nodes"]) >= 1


def test_replicate():

    result = runtime_core.commands.dispatch(

        "ha.replicate",

        {
            "payload": {
                "asset": "Card Hawk"
            },
        },
    )

    assert not result.errors

    replication = result.results["replication"]

    assert "replicated" in replication


def test_failover():

    result = runtime_core.commands.dispatch(
        "ha.failover",
        {},
    )

    assert not result.errors

    failover = result.results["failover"]

    assert failover["status"] in (
        "completed",
        "failed",
    )


def test_statistics():

    result = runtime_core.commands.dispatch(
        "ha.statistics",
        {},
    )

    assert not result.errors

    stats = result.results["ha_stats"]

    assert stats["health"] in (
        "healthy",
        "warning",
    )


if __name__ == "__main__":

    test_ha_service_registered()

    test_bootstrap()

    test_join()

    test_status()

    test_replicate()

    test_failover()

    test_statistics()

    print("\n✔ AletheusOS v3.6 High Availability tests passed.")
