from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalEventBus,
    ConstitutionalGraph,
    ConstitutionalHealth,
    ConstitutionalKind,
    ConstitutionalObject,
    IntelligenceCategory,
    IntelligenceSeverity,
    PlatformDigitalTwin,
    PlatformIntelligenceEngine,
    PlatformServiceDefinition,
    PlatformServiceRegistry,
    RelationshipKind,
    RuntimeExplorer,
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


def build_engine(
    *,
    include_orphan: bool = False,
    fan_in_warning_threshold: int = 5,
) -> tuple[
    PlatformIntelligenceEngine,
    PlatformServiceRegistry,
    ConstitutionalGraph,
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

    if include_orphan:
        graph.add_node(
            ConstitutionalObject.create(
                address="capability.orphan",
                kind=ConstitutionalKind.CAPABILITY,
                canonical_name="Orphan",
                version="1.0.0",
                authority="AletheusOS Constitution",
                owner="Platform Intelligence",
            )
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

    engine = PlatformIntelligenceEngine(
        explorer=explorer,
        graph=graph,
        fan_in_warning_threshold=(fan_in_warning_threshold),
    )

    return engine, registry, graph


def test_analysis_is_immutable_structured_output() -> None:
    engine, _, _ = build_engine()

    analysis = engine.analyze()

    assert 0 <= analysis.constitutional_score <= 100
    assert 0 <= analysis.health_score <= 100
    assert 0 <= analysis.architecture_score <= 100
    assert analysis.metrics["services"] == 2
    assert analysis.metrics["relationships"] == 1


def test_unknown_health_reduces_health_score() -> None:
    engine, _, _ = build_engine()

    analysis = engine.analyze()

    assert analysis.health_score == 70.0
    assert any(
        insight.title == "Services lack health evidence"
        for insight in analysis.insights
    )


def test_all_healthy_services_score_100() -> None:
    engine, registry, graph = build_engine()

    runtime = registry.report_health(
        "service.runtime",
        ConstitutionalHealth.HEALTHY,
    )
    workspace = registry.report_health(
        "service.workspace",
        ConstitutionalHealth.HEALTHY,
    )

    graph.update_node(runtime)
    graph.update_node(workspace)

    analysis = engine.analyze()

    assert analysis.health_score == 100.0


def test_warning_service_generates_insight() -> None:
    engine, registry, graph = build_engine()

    workspace = registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )
    graph.update_node(workspace)

    analysis = engine.analyze()

    health_insights = [
        insight
        for insight in analysis.insights
        if insight.category is IntelligenceCategory.HEALTH
    ]

    assert any(
        insight.severity is IntelligenceSeverity.WARNING for insight in health_insights
    )


def test_warning_service_generates_recommendation() -> None:
    engine, registry, graph = build_engine()

    workspace = registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )
    graph.update_node(workspace)

    analysis = engine.analyze()

    assert any(
        recommendation.title == "Investigate service.workspace"
        for recommendation in analysis.recommendations
    )


def test_orphan_reduces_architecture_score() -> None:
    clean_engine, _, _ = build_engine()
    orphan_engine, _, _ = build_engine(include_orphan=True)

    clean = clean_engine.analyze()
    orphaned = orphan_engine.analyze()

    assert orphaned.architecture_score < clean.architecture_score


def test_orphan_generates_review_recommendation() -> None:
    engine, _, _ = build_engine(include_orphan=True)

    analysis = engine.analyze()

    assert any(
        recommendation.title == "Review orphaned platform objects"
        for recommendation in analysis.recommendations
    )


def test_cycle_is_critical() -> None:
    engine, registry, graph = build_engine()

    third = registry.register(definition("service.third"))
    graph.add_node(third)

    graph.connect(
        source="service.runtime",
        target="service.third",
        kind=RelationshipKind.DEPENDS_ON,
    )
    graph.connect(
        source="service.third",
        target="service.workspace",
        kind=RelationshipKind.DEPENDS_ON,
    )

    analysis = engine.analyze()

    assert analysis.risk_level is (IntelligenceSeverity.CRITICAL)
    assert any(
        insight.title == "Constitutional dependency cycles detected"
        for insight in analysis.insights
    )


def test_high_dependency_concentration_is_detected() -> None:
    engine, registry, graph = build_engine(fan_in_warning_threshold=2)

    second = registry.register(definition("service.second"))
    graph.add_node(second)

    graph.connect(
        source="service.second",
        target="service.runtime",
        kind=RelationshipKind.DEPENDS_ON,
    )

    analysis = engine.analyze()

    assert any(
        insight.title == "High dependency concentration detected"
        for insight in analysis.insights
    )


def test_analysis_serializes() -> None:
    engine, _, _ = build_engine(include_orphan=True)

    payload = engine.analyze().to_dict()

    assert "constitutional_score" in payload
    assert "health_score" in payload
    assert "architecture_score" in payload
    assert isinstance(payload["insights"], list)
    assert isinstance(
        payload["recommendations"],
        list,
    )


def test_invalid_threshold_is_rejected() -> None:
    bus = ConstitutionalEventBus()
    registry = PlatformServiceRegistry(event_bus=bus)
    graph = ConstitutionalGraph()
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

    with pytest.raises(ValueError):
        PlatformIntelligenceEngine(
            explorer=explorer,
            graph=graph,
            fan_in_warning_threshold=0,
        )


def test_engine_is_read_only() -> None:
    engine, _, _ = build_engine()

    forbidden = {
        "register",
        "transition",
        "report_health",
        "remove",
        "connect",
        "publish",
    }

    assert forbidden.isdisjoint(set(dir(engine)))
