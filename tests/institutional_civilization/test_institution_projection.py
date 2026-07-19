from __future__ import annotations

from aletheus.constitutional_graph import ConstitutionalKnowledgeGraph
from aletheus.institutional_civilization import (
    InstitutionProjector,
    InstitutionRegistry,
    canonical_institutions,
)
from aletheus.platform_registry import PlatformRegistry


def test_canonical_catalog_contains_core_institutions():
    records = canonical_institutions()
    institution_ids = {
        record.institution_id
        for record in records
    }

    assert "aletheus.crk" in institution_ids
    assert "aletheus.repository_dna" in institution_ids
    assert "aletheus.ledger" in institution_ids
    assert "aletheus.spa" in institution_ids
    assert "aletheus.watch_tower" in institution_ids
    assert "aletheus.council" in institution_ids
    assert "aletheus.homeostasis" in institution_ids
    assert "aletheus.nimble" in institution_ids
    assert "aletheus.mammoth" in institution_ids
    assert "aletheus.thorx" in institution_ids
    assert "aletheus.breadth" in institution_ids


def test_projects_catalog_into_registry_and_graph():
    institution_registry = InstitutionRegistry()
    platform_registry = PlatformRegistry()
    graph = ConstitutionalKnowledgeGraph()

    projector = InstitutionProjector(
        institution_registry=institution_registry,
        platform_registry=platform_registry,
        constitutional_graph=graph,
    )

    records = canonical_institutions()
    results = projector.project_all(records)

    assert len(results) == len(records)
    assert institution_registry.statistics()["institutions"] == len(records)
    assert platform_registry.statistics()["components"] == len(records)

    graph_stats = graph.statistics()
    assert graph_stats["nodes"] == len(records)
    assert graph_stats["edges"] > 0


def test_platform_registry_preserves_institutional_metadata():
    institution_registry = InstitutionRegistry()
    platform_registry = PlatformRegistry()
    graph = ConstitutionalKnowledgeGraph()

    projector = InstitutionProjector(
        institution_registry=institution_registry,
        platform_registry=platform_registry,
        constitutional_graph=graph,
    )
    projector.project_all(canonical_institutions())

    spa = platform_registry.get("aletheus.spa")

    assert spa is not None
    assert spa.name == "Spectrum Platform Analyzer™"
    assert spa.metadata["institution_id"] == "aletheus.spa"
    assert spa.metadata["pillar"] == "intelligence"
    assert spa.metadata["constitutional_layer"] == "intelligence"


def test_graph_contains_governance_relationships():
    institution_registry = InstitutionRegistry()
    platform_registry = PlatformRegistry()
    graph = ConstitutionalKnowledgeGraph()

    projector = InstitutionProjector(
        institution_registry=institution_registry,
        platform_registry=platform_registry,
        constitutional_graph=graph,
    )
    projector.project_all(canonical_institutions())

    spa_node_id = projector.graph_node_id("aletheus.spa")
    assert spa_node_id is not None

    neighbors = graph.neighbors(spa_node_id)

    assert all("edge" in item for item in neighbors)
    assert all("node" in item for item in neighbors)

    relationships = {
        item["edge"]["relationship"]
        for item in neighbors
    }

    assert "OBSERVED_BY" in relationships
    assert "GOVERNED_BY" in relationships


def test_projection_is_idempotent_for_same_projector():
    institution_registry = InstitutionRegistry()
    platform_registry = PlatformRegistry()
    graph = ConstitutionalKnowledgeGraph()

    projector = InstitutionProjector(
        institution_registry=institution_registry,
        platform_registry=platform_registry,
        constitutional_graph=graph,
    )

    records = canonical_institutions()
    first = projector.project_all(records)
    second = projector.project_all(records)

    assert len(first) == len(second)
    assert institution_registry.statistics()["institutions"] == len(records)
    assert platform_registry.statistics()["components"] == len(records)
    assert graph.statistics()["nodes"] == len(records)
