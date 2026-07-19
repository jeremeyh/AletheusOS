from __future__ import annotations

import pytest

from aletheus.constitutional_graph import ConstitutionalKnowledgeGraph
from aletheus.institutional_civilization import (
    CivilizationProjector,
    CivilizationRegistry,
    DuplicateCivilizationError,
    InstitutionProjector,
    InstitutionRegistry,
    canonical_civilizations,
    canonical_institutions,
)
from aletheus.platform_registry import PlatformRegistry


def test_canonical_civilizations_include_security_domain():
    records = canonical_civilizations()
    ids = {
        record.civilization_id
        for record in records
    }

    assert "aletheus.civilization.governance" in ids
    assert "aletheus.civilization.security" in ids
    assert "aletheus.civilization.intelligence" in ids
    assert "aletheus.civilization.runtime" in ids
    assert "aletheus.civilization.decision" in ids
    assert "aletheus.civilization.experience" in ids
    assert "aletheus.civilization.persistence" in ids
    assert "aletheus.civilization.application" in ids


def test_security_civilization_preserves_defense_chain():
    security = next(
        record
        for record in canonical_civilizations()
        if record.civilization_id
        == "aletheus.civilization.security"
    )

    assert security.institution_ids == (
        "aletheus.watch_tower",
        "aletheus.guardian",
        "aletheus.conclave",
        "aletheus.containment_vault",
        "aletheus.sentinel",
    )


def test_civilization_registry_rejects_duplicates():
    registry = CivilizationRegistry()
    record = canonical_civilizations()[0]

    registry.register(record)

    with pytest.raises(DuplicateCivilizationError):
        registry.register(record)


def test_finds_civilizations_containing_institution():
    registry = CivilizationRegistry()
    registry.register_many(canonical_civilizations())

    memberships = registry.containing_institution(
        "aletheus.watch_tower"
    )

    membership_ids = {
        record.civilization_id
        for record in memberships
    }

    assert "aletheus.civilization.governance" in membership_ids
    assert "aletheus.civilization.security" in membership_ids


def test_projects_civilizations_and_resolved_memberships():
    institution_registry = InstitutionRegistry()
    platform_registry = PlatformRegistry()
    graph = ConstitutionalKnowledgeGraph()

    institution_projector = InstitutionProjector(
        institution_registry=institution_registry,
        platform_registry=platform_registry,
        constitutional_graph=graph,
    )

    institution_projector.project_all(
        canonical_institutions()
    )

    civilization_projector = CivilizationProjector(
        civilization_registry=CivilizationRegistry(),
        institution_registry=institution_registry,
        constitutional_graph=graph,
    )

    for institution in canonical_institutions():
        node_id = institution_projector.graph_node_id(
            institution.institution_id
        )
        assert node_id is not None

        civilization_projector.bind_institution_node(
            institution.institution_id,
            node_id,
        )

    results = civilization_projector.project_all(
        canonical_civilizations()
    )

    assert len(results) == 8
    assert graph.statistics()["nodes"] == len(canonical_institutions()) + len(canonical_civilizations())
    assert any(
        result.resolved_institutions > 0
        for result in results
    )


def test_security_civilization_members_are_resolved():
    institution_registry = InstitutionRegistry()
    platform_registry = PlatformRegistry()
    graph = ConstitutionalKnowledgeGraph()

    institution_projector = InstitutionProjector(
        institution_registry=institution_registry,
        platform_registry=platform_registry,
        constitutional_graph=graph,
    )
    institution_projector.project_all(
        canonical_institutions()
    )

    civilization_projector = CivilizationProjector(
        civilization_registry=CivilizationRegistry(),
        institution_registry=institution_registry,
        constitutional_graph=graph,
    )

    for institution in canonical_institutions():
        node_id = institution_projector.graph_node_id(
            institution.institution_id
        )
        assert node_id is not None

        civilization_projector.bind_institution_node(
            institution.institution_id,
            node_id,
        )

    security = next(
        record
        for record in canonical_civilizations()
        if record.civilization_id
        == "aletheus.civilization.security"
    )

    result = civilization_projector.project(security)

    assert result.resolved_institutions == 5
    assert result.unresolved_institutions == ()

