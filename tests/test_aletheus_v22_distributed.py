from aletheus.runtime import runtime_core


def test_distributed_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Distributed Intelligence Fabric" in diagnostics["services"]


def test_bootstrap_cluster():
    result = runtime_core.commands.dispatch("cluster.bootstrap", {})
    assert not result.errors, result.errors
    assert "cluster" in result.results
    assert len(result.results["cluster"]["nodes"]) >= 1


def test_node_heartbeat_and_status():
    bootstrap = runtime_core.commands.dispatch("cluster.bootstrap", {})
    cluster = bootstrap.results["cluster"]
    node = cluster["nodes"][0]

    heartbeat = runtime_core.commands.dispatch(
        "node.heartbeat",
        {
            "cluster_id": cluster["cluster_id"],
            "node_id": node["node_id"],
        },
    )
    assert not heartbeat.errors, heartbeat.errors
    assert "heartbeat" in heartbeat.results

    status = runtime_core.commands.dispatch(
        "cluster.status",
        {"cluster_id": cluster["cluster_id"]},
    )
    assert not status.errors, status.errors
    assert status.results["cluster_status"]["node_count"] >= 1


def test_cluster_broadcast_and_task():
    bootstrap = runtime_core.commands.dispatch("cluster.bootstrap", {})
    cluster = bootstrap.results["cluster"]

    broadcast = runtime_core.commands.dispatch(
        "cluster.broadcast",
        {
            "cluster_id": cluster["cluster_id"],
            "message": "Distributed fabric broadcast test.",
            "payload": {"test": True},
        },
    )
    assert not broadcast.errors, broadcast.errors
    assert broadcast.results["broadcast"]["status"] == "broadcast"

    task = runtime_core.commands.dispatch(
        "cluster.task.assign",
        {
            "cluster_id": cluster["cluster_id"],
            "title": "Distributed Card Hawk Task",
            "objective": "Run distributed marketplace readiness check.",
            "capability": "marketplace",
        },
    )
    assert not task.errors, task.errors
    assert task.results["task"]["status"] == "completed"


def test_cluster_stats():
    result = runtime_core.commands.dispatch("cluster.stats", {})
    assert not result.errors, result.errors
    assert "cluster_stats" in result.results


if __name__ == "__main__":
    test_distributed_service_registered()
    test_bootstrap_cluster()
    test_node_heartbeat_and_status()
    test_cluster_broadcast_and_task()
    test_cluster_stats()
    print("Aletheus v2.2 Distributed Intelligence Fabric tests passed.")
