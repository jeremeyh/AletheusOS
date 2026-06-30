from aletheus.runtime import runtime_core


def test_runtime_online():
    context = runtime_core.commands.dispatch("runtime.health")
    assert not context.errors
    assert context.results["health"]["status"] == "online"


def test_memory_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Memory Core" in diagnostics["services"]


def test_memory_remember_and_recall():
    write_context = runtime_core.commands.dispatch(
        "memory.remember",
        {
            "key": "test_memory",
            "value": {"message": "hello memory"},
            "namespace": "tests",
            "memory_type": "semantic",
            "tags": ["test", "memory"],
        },
    )

    assert not write_context.errors
    assert "memory_record" in write_context.results

    recall_context = runtime_core.commands.dispatch(
        "memory.recall",
        {
            "namespace": "tests",
            "memory_type": "semantic",
            "tag": "memory",
        },
    )

    assert not recall_context.errors
    records = recall_context.results["memory"]
    assert len(records) >= 1
    assert records[-1]["key"] == "test_memory"


def test_memory_stats():
    context = runtime_core.commands.dispatch("memory.stats")
    assert not context.errors
    assert context.results["memory_stats"]["total_records"] >= 1


if __name__ == "__main__":
    test_runtime_online()
    test_memory_service_registered()
    test_memory_remember_and_recall()
    test_memory_stats()
    print("Aletheus Genesis 0.4 Memory Core tests passed.")
