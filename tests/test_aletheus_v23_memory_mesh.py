from aletheus.runtime import runtime_core


def test_memory_mesh_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Universal Memory Mesh" in diagnostics["services"]


def test_store_retrieve_search_memory():
    stored = runtime_core.commands.dispatch(
        "memory.mesh.store",
        {
            "key": "cardhawk_v23_memory_mesh",
            "value": {"status": "online", "release": "2.3"},
            "namespace": "cardhawk",
            "object_type": "release_record",
            "tags": ["cardhawk", "memory_mesh", "v2.3"],
        },
    )
    assert not stored.errors, stored.errors
    obj = stored.results["memory_object"]
    assert obj["key"] == "cardhawk_v23_memory_mesh"

    retrieved = runtime_core.commands.dispatch(
        "memory.mesh.retrieve",
        {"object_id": obj["object_id"]},
    )
    assert not retrieved.errors, retrieved.errors
    assert retrieved.results["memory_object"]["object_id"] == obj["object_id"]

    search = runtime_core.commands.dispatch(
        "memory.mesh.search",
        {"query": "cardhawk", "namespace": "cardhawk"},
    )
    assert not search.errors, search.errors
    assert len(search.results["results"]) >= 1


def test_snapshot_restore():
    runtime_core.commands.dispatch(
        "memory.mesh.store",
        {
            "key": "snapshot_test",
            "value": "snapshot value",
            "namespace": "tests",
            "tags": ["snapshot"],
        },
    )

    snap = runtime_core.commands.dispatch(
        "memory.mesh.snapshot",
        {"name": "v2.3 Test Snapshot"},
    )
    assert not snap.errors, snap.errors
    snapshot = snap.results["snapshot"]
    assert snapshot["snapshot_id"]

    restored = runtime_core.commands.dispatch(
        "memory.mesh.restore",
        {"snapshot_id": snapshot["snapshot_id"]},
    )
    assert not restored.errors, restored.errors
    assert restored.results["restore"]["restored"] is True


def test_replicate_sync_history_cache():
    stored = runtime_core.commands.dispatch(
        "memory.mesh.store",
        {
            "key": "replication_test",
            "value": {"replicate": True},
            "namespace": "tests",
            "tags": ["replication"],
        },
    )
    obj = stored.results["memory_object"]

    rep = runtime_core.commands.dispatch(
        "memory.mesh.replicate",
        {"object_id": obj["object_id"], "target_node": "Memory Node"},
    )
    assert not rep.errors, rep.errors
    assert rep.results["replication"]["replicated"] >= 1

    sync = runtime_core.commands.dispatch(
        "memory.mesh.sync",
        {"node": "Aletheus Primary Intelligence Cluster"},
    )
    assert not sync.errors, sync.errors
    assert sync.results["sync"]["status"] == "synchronized"

    history = runtime_core.commands.dispatch(
        "memory.mesh.history",
        {"object_id": obj["object_id"]},
    )
    assert not history.errors, history.errors
    assert len(history.results["history"]["versions"]) >= 1

    cache = runtime_core.commands.dispatch(
        "memory.mesh.cache",
        {"object_id": obj["object_id"]},
    )
    assert not cache.errors, cache.errors
    assert cache.results["cache"]["object_id"] == obj["object_id"]


def test_memory_mesh_stats():
    result = runtime_core.commands.dispatch("memory.mesh.stats", {})
    assert not result.errors, result.errors
    assert "memory_mesh_stats" in result.results


if __name__ == "__main__":
    test_memory_mesh_service_registered()
    test_store_retrieve_search_memory()
    test_snapshot_restore()
    test_replicate_sync_history_cache()
    test_memory_mesh_stats()
    print("Aletheus v2.3 Universal Memory Mesh tests passed.")
