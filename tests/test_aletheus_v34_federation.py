from aletheus.runtime import runtime_core


def test_federation_service_registered():

    ctx = runtime_core.commands.dispatch("runtime.diagnostics")

    diagnostics = ctx.results["diagnostics"]

    assert "Aletheus Federated Knowledge Fabric" in diagnostics["services"]


def test_bootstrap():

    result = runtime_core.commands.dispatch(
        "federation.bootstrap",
        {},
    )

    assert not result.errors, result.errors

    stats = result.results["federation"]

    assert stats["health"] == "healthy"


def test_join():

    result = runtime_core.commands.dispatch(

        "federation.join",

        {
            "name": "Houston Runtime",

            "address": "10.0.0.15",

            "capabilities": [
                "reasoning",
                "memory",
            ],

            "services": [
                "Memory",
                "Reasoning",
            ],
        },
    )

    assert not result.errors

    node = result.results["node"]

    assert node["name"] == "Houston Runtime"

    return node["node_id"]


def test_discover():

    result = runtime_core.commands.dispatch(
        "federation.discover",
        {},
    )

    assert not result.errors

    assert isinstance(result.results["nodes"], list)


def test_query():

    result = runtime_core.commands.dispatch(
        "federation.query",
        {},
    )

    assert not result.errors

    federation = result.results["federation"]

    assert "local" in federation

    assert "remote" in federation


def test_broadcast():

    result = runtime_core.commands.dispatch(

        "federation.broadcast",

        {
            "message": "hello federation"
        },
    )

    assert not result.errors

    broadcast = result.results["broadcast"]

    assert broadcast["status"] == "broadcast"


def test_leave():

    discover = runtime_core.commands.dispatch(
        "federation.discover",
        {},
    )

    nodes = discover.results["nodes"]

    if not nodes:
        return

    node_id = nodes[0]["node_id"]

    result = runtime_core.commands.dispatch(

        "federation.leave",

        {
            "node_id": node_id,
        },
    )

    assert not result.errors


def test_statistics():

    result = runtime_core.commands.dispatch(
        "federation.statistics",
        {},
    )

    assert not result.errors

    stats = result.results["federation_stats"]

    assert stats["health"] == "healthy"


if __name__ == "__main__":

    test_federation_service_registered()

    test_bootstrap()

    test_join()

    test_discover()

    test_query()

    test_broadcast()

    test_leave()

    test_statistics()

    print("\n✔ AletheusOS v3.4 Federated Knowledge Fabric tests passed.")
