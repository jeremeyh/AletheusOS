from aletheus.runtime import runtime_core


def test_kernel_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus v2 Autonomous Kernel" in diagnostics["services"]


def test_kernel_boot():
    result = runtime_core.commands.dispatch("kernel.boot", {})
    assert not result.errors, result.errors
    assert "kernel" in result.results
    assert result.results["kernel"]["kernel"]["status"] == "online"


def test_kernel_sync():
    result = runtime_core.commands.dispatch("kernel.sync", {})
    assert not result.errors, result.errors
    assert "kernel" in result.results
    assert result.results["kernel"]["registry_items"] >= 1


def test_kernel_publish_event():
    result = runtime_core.commands.dispatch(
        "kernel.publish",
        {
            "event_type": "test.kernel.event",
            "source": "tests",
            "payload": {"message": "Kernel event bus test."},
        },
    )
    assert not result.errors, result.errors
    assert "event" in result.results
    assert result.results["event"]["status"] == "routed"


def test_kernel_snapshot():
    result = runtime_core.commands.dispatch("kernel.snapshot", {})
    assert not result.errors, result.errors
    assert "snapshot" in result.results


if __name__ == "__main__":
    test_kernel_service_registered()
    test_kernel_boot()
    test_kernel_sync()
    test_kernel_publish_event()
    test_kernel_snapshot()
    print("Aletheus v2.0A Autonomous Kernel tests passed.")
