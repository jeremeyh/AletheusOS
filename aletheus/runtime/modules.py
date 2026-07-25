from __future__ import annotations

from aletheus.runtime.services.service_registry import ServiceRegistry


def register_runtime_services(runtime):
    """
    Legacy v4.5 compatibility layer.

    Ensures the runtime exposes a populated ServiceRegistry under
    `runtime.services`.
    """
    registry = getattr(runtime, "services", None)

    if registry is None or not isinstance(registry, ServiceRegistry):
        registry = ServiceRegistry()
        runtime.services = registry

    # Legacy canonical services expected by older tests.
    defaults = {
        "kernel": object(),
        "governance": object(),
        "memory": object(),
        "reason": object(),
        "knowledge": object(),
        "evidence": object(),
        "risk": object(),
        "prediction": object(),
        "mission": object(),
    }

    for name, service in defaults.items():
        if not registry.has(name):
            registry.register(name, service)

    return registry


def runtime_health(runtime):
    """
    Legacy runtime health view.
    """
    registry = register_runtime_services(runtime)

    return {
        "version": runtime.version,
        "status": runtime.status,
        "services": registry.statistics(),
    }


__all__ = [
    "register_runtime_services",
    "runtime_health",
]
