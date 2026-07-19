from __future__ import annotations

from uuid import UUID

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalEvent,
    ConstitutionalEventBus,
    ConstitutionalEventKind,
    ConstitutionalGraph,
    ConstitutionalHealth,
    PlatformDigitalTwin,
    PlatformServiceDefinition,
    PlatformServiceRegistry,
    RelationshipKind,
    TwinObjectNotFoundError,
    TwinSnapshotNotFoundError,
)


def definition(
    address: str,
    *,
    dependencies: tuple[str, ...] = (),
) -> PlatformServiceDefinition:
    return PlatformServiceDefinition.create(
        address=address,
        canonical_name=address,
        version="1.0.0",
        authority="AletheusOS Constitution",
        owner="Platform Intelligence Fabric",
        dependencies=dependencies,
    )


def build_twin(
    *,
    snapshot_limit: int = 10,
) -> tuple[
    PlatformDigitalTwin,
    PlatformServiceRegistry,
    ConstitutionalGraph,
    ConstitutionalEventBus,
]:
    bus = ConstitutionalEventBus()
    registry = PlatformServiceRegistry(
        event_bus=bus
    )
    graph = ConstitutionalGraph()

    runtime = registry.register(
        definition("service.runtime")
    )
    workspace = registry.register(
        definition(
            "service.workspace",
            dependencies=("service.runtime",),
        )
    )

    graph.add_nodes(
        [runtime, workspace]
    )
    graph.connect(
        source="service.workspace",
        target="service.runtime",
        kind=RelationshipKind.DEPENDS_ON,
    )

    twin = PlatformDigitalTwin(
        service_registry=registry,
        graph=graph,
        event_bus=bus,
        snapshot_limit=snapshot_limit,
    )

    return twin, registry, graph, bus


def test_twin_subscribes_to_event_bus() -> None:
    twin, _, _, _ = build_twin()

    assert isinstance(
        twin.subscription_id,
        UUID,
    )


def test_event_advances_revision() -> None:
    twin, _, _, bus = build_twin()

    initial = twin.revision

    bus.publish(
        ConstitutionalEvent.create(
            kind=ConstitutionalEventKind.PLATFORM_STARTED,
            source="runtime.core",
            subject="runtime.core",
        )
    )

    assert twin.revision == initial + 1
    assert twin.statistics().events_observed == 1


def test_object_query_uses_graph() -> None:
    twin, _, _, _ = build_twin()

    obj = twin.object("service.runtime")

    assert obj.address == "service.runtime"


def test_service_query_uses_registry() -> None:
    twin, _, _, _ = build_twin()

    service = twin.service(
        "service.workspace"
    )

    assert service.address == "service.workspace"


def test_unknown_object_is_rejected() -> None:
    twin, _, _, _ = build_twin()

    with pytest.raises(
        TwinObjectNotFoundError
    ):
        twin.object("service.missing")


def test_dependency_queries() -> None:
    twin, _, _, _ = build_twin()

    assert [
        item.address
        for item in twin.dependencies(
            "service.workspace"
        )
    ] == ["service.runtime"]

    assert [
        item.address
        for item in twin.dependents(
            "service.runtime"
        )
    ] == ["service.workspace"]


def test_impact_returns_upstream_dependents() -> None:
    twin, _, _, _ = build_twin()

    assert [
        item.address
        for item in twin.impact(
            "service.runtime"
        )
    ] == ["service.workspace"]


def test_health_projection_defaults_unknown() -> None:
    twin, _, _, _ = build_twin()

    health = twin.health()

    assert health["state"] == "unknown"
    assert health["total_services"] == 2
    assert health["counts"]["unknown"] == 2


def test_health_projection_detects_warning() -> None:
    twin, registry, _, _ = build_twin()

    registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )

    health = twin.health()

    assert health["state"] == "degraded"
    assert health["unhealthy_services"] == [
        "service.workspace"
    ]


def test_snapshot_is_immutable_and_hashable() -> None:
    twin, _, _, _ = build_twin()

    snapshot = twin.snapshot()

    assert snapshot.revision == twin.revision
    assert len(snapshot.integrity_hash()) == 64

    with pytest.raises(TypeError):
        snapshot.health["state"] = "healthy"  # type: ignore[index]


def test_snapshot_contains_registry_and_graph() -> None:
    twin, _, _, _ = build_twin()

    snapshot = twin.snapshot()

    assert len(snapshot.services) == 2
    assert len(snapshot.nodes) == 2
    assert len(snapshot.relationships) == 1


def test_snapshot_retention_is_bounded() -> None:
    twin, _, _, bus = build_twin(
        snapshot_limit=2
    )

    twin.snapshot()

    bus.publish(
        ConstitutionalEvent.create(
            kind=ConstitutionalEventKind.PLATFORM_STARTED,
            source="runtime.core",
            subject="runtime.core",
        )
    )
    twin.snapshot()

    bus.publish(
        ConstitutionalEvent.create(
            kind=ConstitutionalEventKind.PLATFORM_STOPPED,
            source="runtime.core",
            subject="runtime.core",
        )
    )
    third = twin.snapshot()

    retained = twin.retained_snapshots()

    assert len(retained) == 2
    assert retained[-1] == third


def test_get_snapshot() -> None:
    twin, _, _, _ = build_twin()

    snapshot = twin.snapshot()

    assert twin.get_snapshot(
        snapshot.snapshot_id
    ) == snapshot


def test_unknown_snapshot_is_rejected() -> None:
    twin, _, _, _ = build_twin()

    with pytest.raises(
        TwinSnapshotNotFoundError
    ):
        twin.get_snapshot(UUID(int=0))


def test_snapshot_diff_detects_service_addition() -> None:
    twin, registry, graph, _ = build_twin()

    previous = twin.snapshot()

    diagnostics = registry.register(
        definition("service.diagnostics")
    )
    graph.add_node(diagnostics)

    current = twin.snapshot()
    diff = twin.diff(previous, current)

    assert diff.added_services == (
        "service.diagnostics",
    )
    assert diff.added_nodes == (
        "service.diagnostics",
    )


def test_snapshot_diff_detects_relationship_delta() -> None:
    twin, registry, graph, _ = build_twin()

    diagnostics = registry.register(
        definition("service.diagnostics")
    )
    graph.add_node(diagnostics)

    previous = twin.snapshot()

    graph.connect(
        source="service.diagnostics",
        target="service.runtime",
        kind=RelationshipKind.DEPENDS_ON,
    )

    current = twin.snapshot()
    diff = twin.diff(previous, current)

    assert diff.relationship_delta == 1
    assert diff.topology_changed is True


def test_statistics_are_consistent() -> None:
    twin, registry, _, bus = build_twin()

    registry.report_health(
        "service.runtime",
        ConstitutionalHealth.HEALTHY,
    )
    registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )

    bus.publish(
        ConstitutionalEvent.create(
            kind=ConstitutionalEventKind.PLATFORM_STARTED,
            source="runtime.core",
            subject="runtime.core",
        )
    )

    stats = twin.statistics()

    assert stats.services == 2
    assert stats.nodes == 2
    assert stats.relationships == 1
    assert stats.healthy == 1
    assert stats.warning == 1
    assert stats.events_observed >= 3


def test_current_state_contains_live_projection() -> None:
    twin, _, _, _ = build_twin()

    state = twin.current_state()

    assert state["revision"] == twin.revision
    assert len(state["services"]) == 2
    assert state["graph"]["statistics"]["nodes"] == 2


def test_close_unsubscribes_twin() -> None:
    twin, _, _, bus = build_twin()

    twin.close()

    assert twin.subscription_id is None
    assert (
        bus.statistics().subscriber_count
        == 0
    )
