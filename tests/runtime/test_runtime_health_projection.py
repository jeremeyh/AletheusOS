"""
Runtime health projection regression tests.

Genesis 11.2

Protects the separation between operational health and runtime lifecycle.
"""

from aletheus.runtime.core import AletheusRuntime
from aletheus.runtime.lifecycle.resolver import resolve_runtime_lifecycle


def test_runtime_health_reports_operational_health_and_lifecycle():
    runtime = AletheusRuntime()

    report = runtime.health()

    assert report["health"] == "healthy"
    assert report["lifecycle"] == "online"
    assert report["booted"] is True
    assert report["version"] == runtime.version
    assert isinstance(report["commands"], int)


def test_runtime_health_never_reports_unknown_lifecycle_when_online():
    runtime = AletheusRuntime()

    report = runtime.health()

    assert runtime.status == "online"
    assert report["lifecycle"] != "unknown"
    assert report["lifecycle"] == runtime.status


def test_lifecycle_resolver_prefers_managed_lifecycle_state():
    class State:
        value = "running"

    class Lifecycle:
        state = State()

    class Runtime:
        lifecycle = Lifecycle()
        state = "legacy-state"
        status = "online"

    assert resolve_runtime_lifecycle(Runtime()) == "running"


def test_lifecycle_resolver_supports_legacy_state():
    class Runtime:
        state = "started"
        status = "online"

    assert resolve_runtime_lifecycle(Runtime()) == "started"


def test_lifecycle_resolver_falls_back_to_runtime_status():
    class Runtime:
        status = "online"

    assert resolve_runtime_lifecycle(Runtime()) == "online"


def test_lifecycle_resolver_reports_unknown_without_lifecycle_information():
    class Runtime:
        pass

    assert resolve_runtime_lifecycle(Runtime()) == "unknown"
