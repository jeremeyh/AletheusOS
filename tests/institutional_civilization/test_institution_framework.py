from __future__ import annotations

import pytest

from aletheus.institutional_civilization import (
    ConstitutionalLayer,
    ConstitutionalPillar,
    DuplicateInstitutionError,
    InstitutionalCivilizationEngine,
    InstitutionCriticality,
    InstitutionRecord,
    InstitutionRegistry,
    InstitutionStatus,
    InstitutionValidationError,
)


def spa_record() -> InstitutionRecord:
    return InstitutionRecord(
        institution_id="aletheus.spa",
        canonical_name="Spectrum Platform Analyzer™",
        purpose="Analyze the structural health of AletheusOS.",
        authority="Architectural analysis",
        jurisdiction="Platform architecture",
        constitutional_layer=ConstitutionalLayer.INTELLIGENCE,
        pillar=ConstitutionalPillar.INTELLIGENCE,
        status=InstitutionStatus.IMPLEMENTED,
        criticality=InstitutionCriticality.CRITICAL,
        responsibilities=(
            "Analyze architectural fitness.",
            "Detect structural drift and dependency pressure.",
        ),
        non_responsibilities=(
            "Modify source code.",
            "Make constitutional governance decisions.",
        ),
        consumes=(
            "aletheus.repository_dna",
            "aletheus.constitutional_graph",
        ),
        produces=("architectural_findings",),
        observed_by=("aletheus.watch_tower",),
        governed_by=("aletheus.council",),
        repository_locations=(
            "aletheus/spa",
            "aletheus/spectrum_platform_analyzer",
        ),
        ontology_tags=("architecture", "analysis", "fitness"),
        genesis="12",
    )


def test_registers_and_retrieves_constitutional_institution():
    registry = InstitutionRegistry()

    registered = registry.register(spa_record())

    assert registry.get("aletheus.spa") == registered
    assert registry.by_name("Spectrum Platform Analyzer™") == registered
    assert registry.statistics()["institutions"] == 1


def test_rejects_duplicate_canonical_identity():
    registry = InstitutionRegistry()
    registry.register(spa_record())

    with pytest.raises(DuplicateInstitutionError):
        registry.register(spa_record())


def test_requires_responsibility_and_boundary():
    invalid = InstitutionRecord(
        institution_id="aletheus.invalid",
        canonical_name="Invalid Institution",
        purpose="Demonstrate validation.",
        authority="None",
        jurisdiction="Tests",
        constitutional_layer=ConstitutionalLayer.INTELLIGENCE,
        pillar=ConstitutionalPillar.INTELLIGENCE,
    )

    with pytest.raises(InstitutionValidationError):
        InstitutionRegistry().register(invalid)


def test_engine_preserves_legacy_creation_interface():
    engine = InstitutionalCivilizationEngine()

    legacy = engine.create_institution("legacy-example")

    assert legacy["status"] == "established_legacy"
    assert legacy["constitutional"] is False
    assert engine.statistics()["legacy_records"] == 1


def test_engine_establishes_typed_institution():
    engine = InstitutionalCivilizationEngine()

    established = engine.create_institution(spa_record())

    assert isinstance(established, InstitutionRecord)
    assert engine.get_institution("aletheus.spa") == established
    assert engine.health()["institutions"] == 1


def test_filters_by_pillar_and_layer():
    registry = InstitutionRegistry()
    record = registry.register(spa_record())

    assert registry.by_pillar(
        ConstitutionalPillar.INTELLIGENCE
    ) == (record,)
    assert registry.by_layer(
        ConstitutionalLayer.INTELLIGENCE
    ) == (record,)
