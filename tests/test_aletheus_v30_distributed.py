from aletheus.runtime import runtime_core


def test_cluster_service_registered():
    ctx = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = ctx.results["diagnostics"]
    assert "Aletheus Distributed Runtime Fabric" in diagnostics["services"]


def test_cluster_bootstrap():
    ctx = runtime_core.commands.dispatch("cluster.bootstrap", {})
    assert not ctx.errors, ctx.errors

    stats = ctx.results["cluster"]

    assert stats["clusters"] == 1
    assert stats["nodes"] >= 1


def test_join_leave_node():

    joined = runtime_core.commands.dispatch(
        "cluster.join",
        {
            "node_name": "Marketplace Runtime",
            "capabilities": [
                "marketplace",
                "pricing",
            ],
            "services": [
                "Marketplace Intelligence",
            ],
        },
    )

    assert not joined.errors, joined.errors

    node = joined.results["node"]

    node_id = node["node_id"]

    nodes = runtime_core.commands.dispatch(
        "cluster.nodes",
        {},
    )

    assert not nodes.errors
    assert len(nodes.results["nodes"]["nodes"]) >= 2

    left = runtime_core.commands.dispatch(
        "cluster.leave",
        {
            "node_id": node_id,
        },
    )

    assert not left.errors


def test_leader():

    leader = runtime_core.commands.dispatch(
        "cluster.elect_leader",
        {},
    )

    assert not leader.errors
    assert "leader" in leader.results


def test_heartbeat():

    heartbeat = runtime_core.commands.dispatch(
        "cluster.heartbeat",
        {},
    )

    assert not heartbeat.errors
    assert heartbeat.results["heartbeat"]["heartbeats"] >= 1


def test_status_statistics():

    status = runtime_core.commands.dispatch(
        "cluster.status",
        {},
    )

    assert not status.errors
    assert "cluster_status" in status.results

    stats = runtime_core.commands.dispatch(
        "cluster.statistics",
        {},
    )

    assert not stats.errors
    assert "cluster_stats" in stats.results


if __name__ == "__main__":

    test_cluster_service_registered()
    test_cluster_bootstrap()
    test_join_leave_node()
    test_leader()
    test_heartbeat()
    test_status_statistics()

    print("\n✔ AletheusOS v3.0 Distributed Runtime tests passed.")
