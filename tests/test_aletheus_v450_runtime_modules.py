from aletheus.runtime import runtime_core
from aletheus.runtime.modules import (
    runtime_health,
    register_runtime_services,
)


def test_runtime_modules_import():
    assert runtime_health is not None
    assert register_runtime_services is not None


def test_runtime_health_module():
    health = runtime_health(runtime_core)

    assert health["version"] == runtime_core.version
    assert health["status"] == runtime_core.status
    assert "services" in health


def test_service_registry_available():
    assert hasattr(runtime_core, "services")

    stats = runtime_core.services.statistics()

    assert stats["registered"] >= 9
    assert "kernel" in stats["services"]
    assert "governance" in stats["services"]


if __name__ == "__main__":
    test_runtime_modules_import()
    test_runtime_health_module()
    test_service_registry_available()

    print("\n✔ AletheusOS v4.5.0 Runtime Modules tests passed.")
