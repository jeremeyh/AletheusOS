from __future__ import annotations

from uuid import UUID

import pytest

from aletheus.platform_intelligence import (
    ConstitutionalCycleError,
    ConstitutionalGraph,
    ConstitutionalKind,
    ConstitutionalObject,
    ConstitutionalRelationship,
    GraphNodeAlreadyExistsError,
    GraphNodeInUseError,
    GraphNodeNotFoundError,
    GraphRelationshipAlreadyExistsError,
    GraphRelationshipNotFoundError,
    RelationshipKind,
)


def node(
    address: str,
    *,
    kind: ConstitutionalKind = (ConstitutionalKind.PLATFORM_SERVICE),
) -> ConstitutionalObject:
    return ConstitutionalObject.create(
        address=address,
        kind=kind,
        canonical_name=address,
        version="1.0.0",
        authority="AletheusOS Constitution",
        owner="Platform Intelligence Fabric",
    )


def build_dependency_graph() -> ConstitutionalGraph:
    graph = ConstitutionalGraph()

    graph.add_nodes(
        [
            node("service.runtime"),
            node("service.workspace"),
            node("application.cardhawk"),
            node("service.orphan"),
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

    return graph


def test_add_and_get_node() -> None:
    graph = ConstitutionalGraph()
    runtime = node("service.runtime")

    graph.add_node(runtime)

    assert graph.get_node("service.runtime") == runtime
    assert "service.runtime" in graph


def test_duplicate_node_is_rejected() -> None:
    graph = ConstitutionalGraph()
    runtime = node("service.runtime")

    graph.add_node(runtime)

    with pytest.raises(GraphNodeAlreadyExistsError):
        graph.add_node(runtime)


def test_unknown_node_is_rejected() -> None:
    graph = ConstitutionalGraph()

    with pytest.raises(GraphNodeNotFoundError):
        graph.get_node("service.missing")


def test_update_node_preserves_address() -> None:
    graph = ConstitutionalGraph()
    runtime = node("service.runtime")
    graph.add_node(runtime)

    updated = runtime.with_attributes(role="composition-root")

    graph.update_node(updated)

    assert graph.get_node("service.runtime").attributes["role"] == "composition-root"


def test_add_relationship() -> None:
    graph = ConstitutionalGraph()
    graph.add_nodes(
        [
            node("service.workspace"),
            node("service.runtime"),
        ]
    )

    relationship = graph.connect(
        source="service.workspace",
        target="service.runtime",
        kind=RelationshipKind.DEPENDS_ON,
    )

    assert isinstance(
        relationship.relationship_id,
        UUID,
    )
    assert graph.get_relationship(relationship.relationship_id) == relationship


def test_relationship_requires_existing_nodes() -> None:
    graph = ConstitutionalGraph()
    graph.add_node(node("service.runtime"))

    with pytest.raises(GraphNodeNotFoundError):
        graph.connect(
            source="service.workspace",
            target="service.runtime",
            kind=RelationshipKind.DEPENDS_ON,
        )


def test_duplicate_relationship_is_rejected() -> None:
    graph = ConstitutionalGraph()
    graph.add_nodes(
        [
            node("service.workspace"),
            node("service.runtime"),
        ]
    )

    graph.connect(
        source="service.workspace",
        target="service.runtime",
        kind=RelationshipKind.DEPENDS_ON,
    )

    with pytest.raises(GraphRelationshipAlreadyExistsError):
        graph.connect(
            source="service.workspace",
            target="service.runtime",
            kind=RelationshipKind.DEPENDS_ON,
        )


def test_remove_relationship() -> None:
    graph = build_dependency_graph()
    relationship = graph.relationships()[0]

    removed = graph.remove_relationship(relationship.relationship_id)

    assert removed == relationship

    with pytest.raises(GraphRelationshipNotFoundError):
        graph.get_relationship(relationship.relationship_id)


def test_connected_node_cannot_be_removed() -> None:
    graph = build_dependency_graph()

    with pytest.raises(GraphNodeInUseError):
        graph.remove_node("service.runtime")


def test_force_remove_node_removes_edges() -> None:
    graph = build_dependency_graph()

    graph.remove_node(
        "service.workspace",
        force=True,
    )

    assert "service.workspace" not in graph
    assert graph.relationships() == ()


def test_dependencies_and_dependents() -> None:
    graph = build_dependency_graph()

    assert [item.address for item in graph.dependencies("service.workspace")] == [
        "service.runtime"
    ]

    assert [item.address for item in graph.dependents("service.workspace")] == [
        "application.cardhawk"
    ]


def test_downstream_traversal() -> None:
    graph = build_dependency_graph()

    assert [
        item.address
        for item in graph.downstream(
            "application.cardhawk",
            kinds={RelationshipKind.DEPENDS_ON},
        )
    ] == [
        "service.workspace",
        "service.runtime",
    ]


def test_upstream_traversal() -> None:
    graph = build_dependency_graph()

    assert [
        item.address
        for item in graph.upstream(
            "service.runtime",
            kinds={RelationshipKind.DEPENDS_ON},
        )
    ] == [
        "service.workspace",
        "application.cardhawk",
    ]


def test_shortest_path() -> None:
    graph = build_dependency_graph()

    assert [
        item.address
        for item in graph.shortest_path(
            "application.cardhawk",
            "service.runtime",
        )
    ] == [
        "application.cardhawk",
        "service.workspace",
        "service.runtime",
    ]


def test_unreachable_path_is_empty() -> None:
    graph = build_dependency_graph()

    assert (
        graph.shortest_path(
            "service.runtime",
            "service.orphan",
        )
        == ()
    )


def test_reachability() -> None:
    graph = build_dependency_graph()

    assert graph.is_reachable(
        "application.cardhawk",
        "service.runtime",
    )
    assert not graph.is_reachable(
        "service.runtime",
        "application.cardhawk",
    )


def test_roots_leaves_and_orphans() -> None:
    graph = build_dependency_graph()

    assert [item.address for item in graph.roots()] == [
        "application.cardhawk",
        "service.orphan",
    ]

    assert [item.address for item in graph.leaves()] == [
        "service.orphan",
        "service.runtime",
    ]

    assert [item.address for item in graph.orphans()] == ["service.orphan"]


def test_cycle_detection() -> None:
    graph = ConstitutionalGraph()

    graph.add_nodes(
        [
            node("service.a"),
            node("service.b"),
            node("service.c"),
        ]
    )

    graph.connect(
        source="service.a",
        target="service.b",
        kind=RelationshipKind.DEPENDS_ON,
    )
    graph.connect(
        source="service.b",
        target="service.c",
        kind=RelationshipKind.DEPENDS_ON,
    )
    graph.connect(
        source="service.c",
        target="service.a",
        kind=RelationshipKind.DEPENDS_ON,
    )

    cycles = graph.cycles()

    assert len(cycles) == 1
    assert {str(item) for item in cycles[0]} == {
        "service.a",
        "service.b",
        "service.c",
    }


def test_acyclic_policy_rejects_cycle() -> None:
    graph = ConstitutionalGraph(reject_cycles=True)

    graph.add_nodes(
        [
            node("service.a"),
            node("service.b"),
        ]
    )

    graph.connect(
        source="service.a",
        target="service.b",
        kind=RelationshipKind.DEPENDS_ON,
    )

    with pytest.raises(ConstitutionalCycleError):
        graph.connect(
            source="service.b",
            target="service.a",
            kind=RelationshipKind.DEPENDS_ON,
        )


def test_connected_components() -> None:
    graph = build_dependency_graph()

    components = graph.connected_components()

    assert len(components) == 2
    assert [[node.address for node in component] for component in components] == [
        [
            "application.cardhawk",
            "service.runtime",
            "service.workspace",
        ],
        ["service.orphan"],
    ]


def test_statistics_are_consistent() -> None:
    graph = build_dependency_graph()

    stats = graph.statistics()

    assert stats.nodes == 4
    assert stats.relationships == 2
    assert stats.roots == 2
    assert stats.leaves == 2
    assert stats.orphans == 1
    assert stats.cycles == 0
    assert stats.connected_components == 2
    assert stats.maximum_depth == 2
    assert stats.average_out_degree == 0.5
    assert stats.average_in_degree == 0.5
    assert stats.relationships_by_kind["depends_on"] == 2


def test_snapshot_is_deterministic() -> None:
    graph = build_dependency_graph()

    first = graph.snapshot()
    second = graph.snapshot()

    assert first == second
    assert first["statistics"]["nodes"] == 4
    assert first["topology"]["orphans"] == ["service.orphan"]


def test_relationship_object_can_be_added() -> None:
    graph = ConstitutionalGraph()

    graph.add_nodes(
        [
            node("service.runtime"),
            node("service.workspace"),
        ]
    )

    relationship = ConstitutionalRelationship.create(
        source="service.workspace",
        target="service.runtime",
        kind=RelationshipKind.DEPENDS_ON,
    )

    assert graph.add_relationship(relationship) == relationship
