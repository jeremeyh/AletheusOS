from types import SimpleNamespace

from aletheus.runtime.composition import RuntimeCompositionRoot
from aletheus.runtime.kernel import RuntimeKernel
from aletheus.runtime.lifecycle.state import RuntimeLifecycleState


def test_build_kernel_returns_runtime_kernel():
    root = RuntimeCompositionRoot()

    kernel = root.build_kernel()

    assert isinstance(kernel, RuntimeKernel)
    assert kernel.orchestrator is not None
    assert kernel.boot_pipeline is not None


def test_boot_attaches_kernel_and_delegates(monkeypatch):
    root = RuntimeCompositionRoot()
    runtime = SimpleNamespace()

    kernel = root.build_kernel()

    called = {}

    def fake_boot(candidate):
        called["runtime"] = candidate
        called["kernel"] = candidate.kernel
        return candidate

    monkeypatch.setattr(kernel, "boot", fake_boot)
    monkeypatch.setattr(root, "build_kernel", lambda: kernel)

    result = root.boot(runtime)

    assert result is runtime
    assert called["runtime"] is runtime
    assert called["kernel"] is kernel
    assert runtime.kernel is kernel


def test_kernel_boot_transitions_runtime_online(monkeypatch):
    root = RuntimeCompositionRoot()
    kernel = root.build_kernel()

    runtime = SimpleNamespace()

    monkeypatch.setattr(
        kernel.boot_pipeline,
        "run",
        lambda candidate: candidate,
    )

    result = kernel.boot(runtime)

    assert result is runtime
    assert (
        kernel.orchestrator.lifecycle.state
        is RuntimeLifecycleState.ONLINE
    )
