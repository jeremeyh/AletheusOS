from __future__ import annotations

from aletheus.platform_intelligence import (
    ConstitutionalEvent,
    ConstitutionalEventBus,
    ConstitutionalEventKind,
    ConstitutionalGraph,
    ConstitutionalHealth,
    PlatformDigitalTwin,
    PlatformIntelligenceEngine,
    PlatformServiceDefinition,
    PlatformServiceRegistry,
    RelationshipKind,
    RuntimeExplorer,
    RuntimeIntelligenceOrchestrator,
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
        owner="Platform Intelligence",
        dependencies=dependencies,
    )


def build_orchestrator() -> tuple[
    RuntimeIntelligenceOrchestrator,
    PlatformServiceRegistry,
    ConstitutionalGraph,
    ConstitutionalEventBus,
]:
    bus = ConstitutionalEventBus()
    registry = PlatformServiceRegistry(event_bus=bus)
    graph = ConstitutionalGraph()

    runtime = registry.register(definition("service.runtime"))
    workspace = registry.register(
        definition(
            "service.workspace",
            dependencies=("service.runtime",),
        )
    )

    graph.add_nodes([runtime, workspace])

    graph.connect(
        source="service.workspace",
        target="service.runtime",
        kind=RelationshipKind.DEPENDS_ON,
    )

    twin = PlatformDigitalTwin(
        service_registry=registry,
        graph=graph,
        event_bus=bus,
    )

    explorer = RuntimeExplorer(
        twin=twin,
        graph=graph,
        service_registry=registry,
    )

    intelligence = PlatformIntelligenceEngine(
        explorer=explorer,
        graph=graph,
    )

    orchestrator = RuntimeIntelligenceOrchestrator(
        service_registry=registry,
        graph=graph,
        event_bus=bus,
        digital_twin=twin,
        explorer=explorer,
        intelligence_engine=intelligence,
    )

    return orchestrator, registry, graph, bus


def test_overview_composes_platform_state() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    overview = orchestrator.overview()

    assert overview.twin_revision == 0
    assert overview.services["statistics"]["registered"] == 2
    assert overview.graph["statistics"]["relationships"] == 1
    assert overview.intelligence["constitutional_score"] >= 0


def test_overview_serializes() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    payload = orchestrator.overview().to_dict()

    assert "runtime" in payload
    assert "services" in payload
    assert "graph" in payload
    assert "events" in payload
    assert "health" in payload
    assert "constitution" in payload
    assert "intelligence" in payload


def test_health_summary_defaults_unknown() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    health = orchestrator.health_summary()

    assert health.state == "unknown"
    assert health.total_services == 2
    assert health.unknown == 2


def test_health_summary_reflects_registry() -> None:
    orchestrator, registry, graph, _ = build_orchestrator()

    runtime = registry.report_health(
        "service.runtime",
        ConstitutionalHealth.HEALTHY,
    )
    workspace = registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )

    graph.update_node(runtime)
    graph.update_node(workspace)

    health = orchestrator.health_summary()

    assert health.state == "degraded"
    assert health.healthy == 1
    assert health.warning == 1
    assert health.unhealthy_services == ("service.workspace",)


def test_constitutional_state_is_satisfied() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    state = orchestrator.constitutional_state()

    assert state.satisfied is True
    assert state.cycles == 0
    assert state.broken_dependencies == 0
    assert state.checks["no_cycles"] is True


def test_orphan_breaks_constitutional_state() -> None:
    orchestrator, registry, graph, _ = build_orchestrator()

    diagnostics = registry.register(definition("service.diagnostics"))
    graph.add_node(diagnostics)

    state = orchestrator.constitutional_state()

    assert state.satisfied is False
    assert state.orphans == 1
    assert state.checks["no_orphans"] is False


def test_event_summary_exposes_latest_event() -> None:
    orchestrator, _, _, bus = build_orchestrator()

    published = bus.publish(
        ConstitutionalEvent.create(
            kind=(ConstitutionalEventKind.PLATFORM_STARTED),
            source="runtime.core",
            subject="runtime.core",
        )
    )

    summary = orchestrator.event_summary()

    assert summary["history_size"] >= 1
    assert summary["latest"]["event_id"] == str(published.event_id)


def test_snapshot_delegates_to_twin() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    snapshot = orchestrator.snapshot()

    assert len(snapshot.services) == 2
    assert len(snapshot.nodes) == 2
    assert len(orchestrator.retained_snapshots()) == 1


def test_service_inventory_is_complete() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    inventory = orchestrator.service_inventory()

    assert inventory["statistics"]["registered"] == 2
    assert len(inventory["services"]) == 2


def test_dependency_summary_is_complete() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    summary = orchestrator.dependency_summary()

    assert len(summary["nodes"]) == 2
    assert len(summary["relationships"]) == 1
    assert summary["statistics"]["connected_components"] == 1


def test_intelligence_summary_is_structured() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    analysis = orchestrator.intelligence_summary()

    assert 0 <= analysis.health_score <= 100
    assert 0 <= analysis.architecture_score <= 100


def test_revision_tracks_twin_events() -> None:
    orchestrator, _, _, bus = build_orchestrator()

    assert orchestrator.revision == 0

    bus.publish(
        ConstitutionalEvent.create(
            kind=(ConstitutionalEventKind.PLATFORM_STARTED),
            source="runtime.core",
            subject="runtime.core",
        )
    )

    assert orchestrator.revision == 1


def test_orchestrator_is_read_only() -> None:
    orchestrator, _, _, _ = build_orchestrator()

    forbidden = {
        "register",
        "transition",
        "report_health",
        "remove",
        "connect",
        "publish",
        "execute",
    }

    assert forbidden.isdisjoint(set(dir(orchestrator)))
