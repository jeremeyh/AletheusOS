from aletheus.runtime import runtime_core


def test_runtime_exists():
    """Runtime singleton is available."""
    assert runtime_core is not None


def test_service_registry_exists():
    """Runtime exposes a ServiceRegistry."""
    assert hasattr(runtime_core, "services")
    assert runtime_core.services is not None


def test_service_registry_statistics():
    """Registry returns consistent statistics."""

    stats = runtime_core.services.statistics()

    assert "registered" in stats
    assert "services" in stats

    assert stats["registered"] == len(stats["services"])

    # Genesis 8 baseline
    assert stats["registered"] >= 25


def test_core_runtime_services_registered():
    """Critical platform services are registered."""

    services = runtime_core.services.statistics()["services"]

    expected = {
        "kernel",
        "governance",
        "metrics",
        "events",
    }

    assert expected.issubset(set(services))


def test_foundational_platform_services_registered():
    """Genesis platform capabilities are available."""

    services = runtime_core.services.statistics()["services"]

    expected = {
        "Aletheus Runtime Core",
        "Aletheus Memory Core",
        "Aletheus Knowledge Graph Engine",
        "Aletheus Founder Workspace",
        "Aletheus Founder Copilot",
    }

    assert expected.issubset(set(services))
