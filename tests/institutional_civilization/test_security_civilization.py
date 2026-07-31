from __future__ import annotations

from aletheus.constitutional_graph import ConstitutionalKnowledgeGraph
from aletheus.institutional_civilization import (
    CANONICAL_SECURITY_RELATIONSHIPS,
    InstitutionProjector,
    InstitutionRegistry,
    SecurityCivilizationProjector,
    canonical_institutions,
)
from aletheus.platform_registry import PlatformRegistry


def build_security_projection():
    institution_registry = InstitutionRegistry()
    platform_registry = PlatformRegistry()
    graph = ConstitutionalKnowledgeGraph()

    institution_projector = InstitutionProjector(
        institution_registry=institution_registry,
        platform_registry=platform_registry,
        constitutional_graph=graph,
    )
    institution_projector.project_all(canonical_institutions())

    security_projector = SecurityCivilizationProjector(
        institution_projector=institution_projector,
        constitutional_graph=graph,
    )

    return (
        institution_registry,
        platform_registry,
        graph,
        institution_projector,
        security_projector,
    )


def test_security_institutions_are_canonical():
    records = {record.institution_id: record for record in canonical_institutions()}

    assert "aletheus.watch_tower" in records
    assert "aletheus.guardian" in records
    assert "aletheus.conclave" in records
    assert "aletheus.containment_vault" in records
    assert "aletheus.sentinel" in records

    assert records["aletheus.guardian"].canonical_name == "Guardian™"
    assert records["aletheus.conclave"].canonical_name == "Conclave™"
    assert records["aletheus.containment_vault"].canonical_name == "Containment Vault™"
    assert records["aletheus.sentinel"].canonical_name == "Sentinel™"


def test_canonical_catalog_contains_fifteen_institutions():
    assert len(canonical_institutions()) == 15


def test_projects_complete_security_defense_chain():
    (
        _,
        _,
        graph,
        _,
        security_projector,
    ) = build_security_projection()

    edges = security_projector.project()

    assert len(edges) == len(CANONICAL_SECURITY_RELATIONSHIPS)

    relationships = {edge["relationship"] for edge in edges}

    assert "ESCALATES_TO" in relationships
    assert "REQUESTS_CONTAINMENT_FROM" in relationships
    assert "QUARANTINES_IN" in relationships
    assert "PROTECTS" in relationships
    assert "PRESERVES_CHAIN_OF_CUSTODY_IN" in relationships


def test_watch_tower_escalates_to_guardian():
    (
        _,
        _,
        graph,
        institution_projector,
        security_projector,
    ) = build_security_projection()

    security_projector.project()

    watch_tower_node = institution_projector.graph_node_id("aletheus.watch_tower")
    assert watch_tower_node is not None

    neighbors = graph.neighbors(watch_tower_node)

    assert any(
        item["edge"]["relationship"] == "ESCALATES_TO"
        and item["node"]["data"]["institution_id"] == "aletheus.guardian"
        for item in neighbors
    )


def test_conclave_quarantines_in_containment_vault():
    (
        _,
        _,
        graph,
        institution_projector,
        security_projector,
    ) = build_security_projection()

    security_projector.project()

    conclave_node = institution_projector.graph_node_id("aletheus.conclave")
    assert conclave_node is not None

    neighbors = graph.neighbors(conclave_node)

    assert any(
        item["edge"]["relationship"] == "QUARANTINES_IN"
        and item["node"]["data"]["institution_id"] == "aletheus.containment_vault"
        for item in neighbors
    )


def test_security_projection_is_idempotent():
    (
        _,
        _,
        _,
        _,
        security_projector,
    ) = build_security_projection()

    first = security_projector.project()
    second = security_projector.project()

    assert len(first) == len(CANONICAL_SECURITY_RELATIONSHIPS)
    assert second == ()
