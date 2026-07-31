from __future__ import annotations

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalEventBus,
    ConstitutionalGraph,
    ConstitutionalHealth,
    ConstitutionalKind,
    ConstitutionalObject,
    ConstitutionalState,
    ExplorerObjectNotFoundError,
    ExplorerQueryError,
    PlatformDigitalTwin,
    PlatformServiceDefinition,
    PlatformServiceRegistry,
    RelationshipKind,
    RuntimeExplorer,
)


def definition(
    address: str,
    *,
    owner: str = "Platform Intelligence",
    dependencies: tuple[str, ...] = (),
) -> PlatformServiceDefinition:
    return PlatformServiceDefinition.create(
        address=address,
        canonical_name=address,
        version="1.0.0",
        authority="AletheusOS Constitution",
        owner=owner,
        dependencies=dependencies,
    )


def build_explorer() -> tuple[
    RuntimeExplorer,
    PlatformServiceRegistry,
    ConstitutionalGraph,
    PlatformDigitalTwin,
]:
    bus = ConstitutionalEventBus()
    registry = PlatformServiceRegistry(event_bus=bus)
    graph = ConstitutionalGraph()

    runtime = registry.register(
        definition(
            "service.runtime",
            owner="Runtime",
        )
    )
    workspace = registry.register(
        definition(
            "service.workspace",
            owner="Workspace Engine",
            dependencies=("service.runtime",),
        )
    )

    graph.add_nodes(
        [
            runtime,
            workspace,
            ConstitutionalObject.create(
                address="application.cardhawk",
                kind=ConstitutionalKind.APPLICATION,
                canonical_name="Card Hawk",
                version="1.0.0",
                authority="AletheusOS Constitution",
                owner="Card Hawk",
            ),
            ConstitutionalObject.create(
                address="capability.orphan",
                kind=ConstitutionalKind.CAPABILITY,
                canonical_name="Orphan Capability",
                version="1.0.0",
                authority="AletheusOS Constitution",
                owner="Platform Intelligence",
            ),
        ]
    )

    graph.connect(
        source="service.workspace",
        target="service.runtime",
        kind=RelationshipKind.DEPENDS_ON,
    )
    graph.connect(
        source="application.cardhawk",
        target="service.workspace",
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

    return explorer, registry, graph, twin


def test_object_lookup() -> None:
    explorer, _, _, _ = build_explorer()

    assert explorer.object("service.runtime").address == "service.runtime"


def test_unknown_object_is_rejected() -> None:
    explorer, _, _, _ = build_explorer()

    with pytest.raises(ExplorerObjectNotFoundError):
        explorer.object("service.missing")


def test_objects_are_deduplicated() -> None:
    explorer, _, _, _ = build_explorer()

    assert [item.address for item in explorer.objects()] == [
        "application.cardhawk",
        "capability.orphan",
        "service.runtime",
        "service.workspace",
    ]


def test_find_by_kind() -> None:
    explorer, _, _, _ = build_explorer()

    assert [
        item.address for item in explorer.find_by_kind(ConstitutionalKind.APPLICATION)
    ] == ["application.cardhawk"]


def test_find_by_owner() -> None:
    explorer, _, _, _ = build_explorer()

    assert [item.address for item in explorer.find_by_owner("workspace")] == [
        "service.workspace"
    ]


def test_find_by_authority() -> None:
    explorer, _, _, _ = build_explorer()

    assert len(explorer.find_by_authority("AletheusOS")) == 4


def test_find_by_state() -> None:
    explorer, registry, graph, _ = build_explorer()

    initializing = registry.transition(
        "service.runtime",
        ConstitutionalState.INITIALIZING,
    )
    graph.update_node(initializing)

    assert [
        item.address
        for item in explorer.find_by_state(ConstitutionalState.INITIALIZING)
    ] == ["service.runtime"]


def test_find_by_health() -> None:
    explorer, registry, graph, _ = build_explorer()

    warning = registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )
    graph.update_node(warning)

    assert [
        item.address for item in explorer.find_by_health(ConstitutionalHealth.WARNING)
    ] == ["service.workspace"]


def test_unhealthy_projection() -> None:
    explorer, registry, graph, _ = build_explorer()

    warning = registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )
    graph.update_node(warning)

    assert [item.address for item in explorer.unhealthy()] == ["service.workspace"]


def test_search_ranks_exact_address_highest() -> None:
    explorer, _, _, _ = build_explorer()

    results = explorer.search("service.runtime")

    assert results[0].object.address == ("service.runtime")
    assert results[0].score >= 100


def test_search_matches_partial_text() -> None:
    explorer, _, _, _ = build_explorer()

    results = explorer.search("card")

    assert [result.object.address for result in results] == ["application.cardhawk"]


def test_empty_search_returns_empty_result() -> None:
    explorer, _, _, _ = build_explorer()

    assert explorer.search("   ") == ()


def test_cql_kind_query() -> None:
    explorer, _, _, _ = build_explorer()

    assert [item.address for item in explorer.query("kind:application")] == [
        "application.cardhawk"
    ]


def test_cql_combines_terms() -> None:
    explorer, _, _, _ = build_explorer()

    assert [
        item.address for item in explorer.query("kind:platform_service owner:workspace")
    ] == ["service.workspace"]


def test_invalid_cql_field_is_rejected() -> None:
    explorer, _, _, _ = build_explorer()

    with pytest.raises(ExplorerQueryError):
        explorer.query("unsupported:value")


def test_dependencies() -> None:
    explorer, _, _, _ = build_explorer()

    assert [item.address for item in explorer.dependencies("service.workspace")] == [
        "service.runtime"
    ]


def test_transitive_dependencies() -> None:
    explorer, _, _, _ = build_explorer()

    assert [
        item.address
        for item in explorer.dependencies(
            "application.cardhawk",
            transitive=True,
        )
    ] == [
        "service.workspace",
        "service.runtime",
    ]


def test_dependents() -> None:
    explorer, _, _, _ = build_explorer()

    assert [item.address for item in explorer.dependents("service.runtime")] == [
        "service.workspace"
    ]


def test_impact_analysis() -> None:
    explorer, _, _, _ = build_explorer()

    impact = explorer.impact("service.runtime")

    assert [item.address for item in impact.direct_dependents] == ["service.workspace"]

    assert [item.address for item in impact.transitive_dependents] == [
        "service.workspace",
        "application.cardhawk",
    ]

    assert impact.affected_count == 2


def test_shortest_path() -> None:
    explorer, _, _, _ = build_explorer()

    assert [
        item.address
        for item in explorer.path(
            "application.cardhawk",
            "service.runtime",
        )
    ] == [
        "application.cardhawk",
        "service.workspace",
        "service.runtime",
    ]


def test_orphan_query() -> None:
    explorer, _, _, _ = build_explorer()

    assert [item.address for item in explorer.orphans()] == ["capability.orphan"]


def test_snapshot_access_and_diff() -> None:
    explorer, registry, graph, _ = build_explorer()

    previous = explorer.snapshot()

    diagnostics = registry.register(definition("service.diagnostics"))
    graph.add_node(diagnostics)

    current = explorer.snapshot()
    diff = explorer.diff(
        previous,
        current,
    )

    assert diff.added_services == ("service.diagnostics",)
    assert len(explorer.snapshots()) == 2


def test_statistics_are_consistent() -> None:
    explorer, registry, graph, _ = build_explorer()

    warning = registry.report_health(
        "service.workspace",
        ConstitutionalHealth.WARNING,
    )
    graph.update_node(warning)

    stats = explorer.statistics()

    assert stats.objects == 4
    assert stats.services == 2
    assert stats.relationships == 2
    assert stats.unhealthy == 1
    assert stats.orphans == 1
    assert stats.cycles == 0
    assert stats.objects_by_kind["platform_service"] == 2


def test_explorer_is_read_only() -> None:
    explorer, _, _, _ = build_explorer()

    forbidden = {
        "register",
        "transition",
        "report_health",
        "remove",
        "connect",
        "publish",
    }

    assert forbidden.isdisjoint(set(dir(explorer)))
