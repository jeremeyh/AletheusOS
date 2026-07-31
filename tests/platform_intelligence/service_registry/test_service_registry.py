from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalEventBus,
    ConstitutionalEventKind,
    ConstitutionalHealth,
    ConstitutionalState,
    PlatformServiceDefinition,
    PlatformServiceRegistry,
    ServiceAlreadyRegisteredError,
    ServiceDependencyError,
    ServiceInUseError,
    ServiceNotFoundError,
)


def definition(
    address: str,
    *,
    dependencies: tuple[str, ...] = (),
) -> PlatformServiceDefinition:
    return PlatformServiceDefinition.create(
        address=address,
        canonical_name=address.replace(".", " ").title(),
        version="1.0.0",
        authority="AletheusOS Constitution",
        owner="Platform Intelligence Fabric",
        dependencies=dependencies,
    )


def test_register_service() -> None:
    registry = PlatformServiceRegistry()

    service = registry.register(definition("service.runtime"))

    assert service.address == "service.runtime"
    assert service.state is ConstitutionalState.REGISTERED
    assert registry.get("service.runtime") == service


def test_duplicate_service_is_rejected() -> None:
    registry = PlatformServiceRegistry()
    service_definition = definition("service.runtime")

    registry.register(service_definition)

    with pytest.raises(ServiceAlreadyRegisteredError):
        registry.register(service_definition)


def test_unknown_service_is_rejected() -> None:
    registry = PlatformServiceRegistry()

    with pytest.raises(ServiceNotFoundError):
        registry.get("service.unknown")


def test_missing_dependency_is_rejected() -> None:
    registry = PlatformServiceRegistry()

    with pytest.raises(ServiceDependencyError):
        registry.register(
            definition(
                "service.workspace",
                dependencies=("service.runtime",),
            )
        )


def test_dependency_can_be_registered() -> None:
    registry = PlatformServiceRegistry()

    registry.register(definition("service.runtime"))
    registry.register(
        definition(
            "service.workspace",
            dependencies=("service.runtime",),
        )
    )

    assert [str(item) for item in registry.dependencies_of("service.workspace")] == [
        "service.runtime"
    ]

    assert [str(item) for item in registry.dependents_of("service.runtime")] == [
        "service.workspace"
    ]


def test_register_many_resolves_dependency_order() -> None:
    registry = PlatformServiceRegistry()

    registered = registry.register_many(
        [
            definition(
                "service.workspace",
                dependencies=("service.runtime",),
            ),
            definition("service.runtime"),
        ]
    )

    assert [service.address for service in registered] == [
        "service.runtime",
        "service.workspace",
    ]


def test_register_many_rejects_unresolvable_graph() -> None:
    registry = PlatformServiceRegistry()

    with pytest.raises(ServiceDependencyError):
        registry.register_many(
            [
                definition(
                    "service.a",
                    dependencies=("service.b",),
                ),
                definition(
                    "service.b",
                    dependencies=("service.a",),
                ),
            ]
        )


def test_registration_publishes_events() -> None:
    bus = ConstitutionalEventBus()
    registry = PlatformServiceRegistry(event_bus=bus)

    registry.register(definition("service.runtime"))

    kinds = [event.kind for event in bus.history()]

    assert ConstitutionalEventKind.OBJECT_REGISTERED in kinds
    assert ConstitutionalEventKind.SERVICE_REGISTERED in kinds


def test_transition_updates_service() -> None:
    registry = PlatformServiceRegistry()
    registry.register(definition("service.runtime"))

    initializing = registry.transition(
        "service.runtime",
        ConstitutionalState.INITIALIZING,
    )
    starting = registry.transition(
        "service.runtime",
        ConstitutionalState.STARTING,
    )
    running = registry.transition(
        "service.runtime",
        ConstitutionalState.RUNNING,
        health=ConstitutionalHealth.HEALTHY,
    )

    assert initializing.state is (ConstitutionalState.INITIALIZING)
    assert starting.state is ConstitutionalState.STARTING
    assert running.state is ConstitutionalState.RUNNING
    assert running.health is ConstitutionalHealth.HEALTHY


def test_running_transition_publishes_service_started() -> None:
    bus = ConstitutionalEventBus()
    registry = PlatformServiceRegistry(event_bus=bus)

    registry.register(definition("service.runtime"))
    registry.transition(
        "service.runtime",
        ConstitutionalState.INITIALIZING,
    )
    registry.transition(
        "service.runtime",
        ConstitutionalState.STARTING,
    )
    registry.transition(
        "service.runtime",
        ConstitutionalState.RUNNING,
    )

    assert any(
        event.kind is ConstitutionalEventKind.SERVICE_STARTED for event in bus.history()
    )


def test_health_reporting_updates_service() -> None:
    registry = PlatformServiceRegistry()
    registry.register(definition("service.runtime"))

    updated = registry.report_health(
        "service.runtime",
        ConstitutionalHealth.WARNING,
        metrics={"latency_ms": 42},
    )

    assert updated.health is ConstitutionalHealth.WARNING
    assert updated.metrics["latency_ms"] == 42


def test_health_reporting_publishes_event() -> None:
    bus = ConstitutionalEventBus()
    registry = PlatformServiceRegistry(event_bus=bus)

    registry.register(definition("service.runtime"))
    registry.report_health(
        "service.runtime",
        ConstitutionalHealth.WARNING,
    )

    assert any(
        event.kind is ConstitutionalEventKind.HEALTH_CHANGED for event in bus.history()
    )


def test_service_with_dependents_cannot_be_removed() -> None:
    registry = PlatformServiceRegistry()

    registry.register(definition("service.runtime"))
    registry.register(
        definition(
            "service.workspace",
            dependencies=("service.runtime",),
        )
    )

    with pytest.raises(ServiceInUseError):
        registry.remove("service.runtime")


def test_force_remove_detaches_dependency() -> None:
    registry = PlatformServiceRegistry()

    registry.register(definition("service.runtime"))
    registry.register(
        definition(
            "service.workspace",
            dependencies=("service.runtime",),
        )
    )

    registry.remove(
        "service.runtime",
        force=True,
    )

    assert not registry.contains("service.runtime")
    assert registry.dependencies_of("service.workspace") == ()


def test_statistics_are_consistent() -> None:
    registry = PlatformServiceRegistry()

    registry.register(definition("service.runtime"))
    registry.register(
        definition(
            "service.workspace",
            dependencies=("service.runtime",),
        )
    )

    registry.transition(
        "service.runtime",
        ConstitutionalState.INITIALIZING,
    )
    registry.transition(
        "service.runtime",
        ConstitutionalState.STARTING,
    )
    registry.transition(
        "service.runtime",
        ConstitutionalState.RUNNING,
        health=ConstitutionalHealth.HEALTHY,
    )

    registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )

    stats = registry.statistics()

    assert stats.registered == 2
    assert stats.running == 1
    assert stats.unhealthy == 1
    assert stats.dependency_edges == 1


def test_snapshot_contains_relationships() -> None:
    registry = PlatformServiceRegistry()

    registry.register(definition("service.runtime"))
    registry.register(
        definition(
            "service.workspace",
            dependencies=("service.runtime",),
        )
    )

    snapshot = registry.snapshot()
    services = {item["identity"]["address"]: item for item in snapshot["services"]}

    assert services["service.workspace"]["dependencies"] == ["service.runtime"]

    assert services["service.runtime"]["dependents"] == ["service.workspace"]
