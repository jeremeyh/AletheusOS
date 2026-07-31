from __future__ import annotations

import pytest

from aletheus.constitutional_cognition import (
    ContributionStance,
    EngineContribution,
    FunctionalCognitiveParticipant,
    MultiplicitousIntelligenceMesh,
)
from aletheus.constitutional_instrumentation import (
    ConstitutionalInstrumentBus,
    ConstitutionalInstrumentRegistry,
    DuplicateInstrumentError,
    InstrumentDefinition,
    InstrumentKind,
    InstrumentSignal,
    InstrumentSignalType,
    InstrumentStatus,
    build_cognition_instrumentation,
    canonical_cognition_instruments,
)

ASSERTION = "card.value.increases"


def participant(
    engine_id: str,
    stance: ContributionStance,
    confidence: float,
):
    def evaluate(payload):
        return EngineContribution(
            engine_id=engine_id,
            assertion_key=ASSERTION,
            stance=stance,
            confidence=confidence,
            evidence_count=1,
            evidence=(
                {
                    "source": (f"{engine_id}.evidence"),
                },
            ),
        )

    return FunctionalCognitiveParticipant(
        engine_id=engine_id,
        evaluator=evaluate,
    )


def test_canonical_instrument_catalog_is_complete():
    instruments = canonical_cognition_instruments()

    instrument_ids = {item.instrument_id for item in instruments}

    assert len(instruments) == 8
    assert "aletheus.instrument.confidence" in instrument_ids
    assert "aletheus.instrument.truth" in instrument_ids
    assert "aletheus.instrument.timeline" in instrument_ids


def test_registry_rejects_duplicate_instrument():
    registry = ConstitutionalInstrumentRegistry()

    definition = InstrumentDefinition(
        instrument_id="test.instrument",
        canonical_name="Test Instrument",
        kind=InstrumentKind.GAUGE,
        signal_source="test",
    )

    registry.register(definition)

    with pytest.raises(DuplicateInstrumentError):
        registry.register(definition)


def test_bus_projects_current_instrument_state():
    registry = ConstitutionalInstrumentRegistry()

    registry.register(
        InstrumentDefinition(
            instrument_id="test.confidence",
            canonical_name="Test Confidence",
            kind=InstrumentKind.CONFIDENCE,
            signal_source="test",
        )
    )

    bus = ConstitutionalInstrumentBus(registry=registry)

    bus.publish(
        InstrumentSignal(
            instrument_id="test.confidence",
            signal_type=(InstrumentSignalType.CONFIDENCE_CHANGED),
            source_identity="test.engine",
            value=0.82,
            confidence=0.82,
            status=InstrumentStatus.STABLE,
        )
    )

    state = bus.state("test.confidence")

    assert state.current_value == 0.82
    assert state.normalized_value == 0.82
    assert state.status == (InstrumentStatus.STABLE)
    assert state.update_count == 1


def test_bus_notifies_instrument_subscribers():
    registry = ConstitutionalInstrumentRegistry()

    registry.register(
        InstrumentDefinition(
            instrument_id="test.pulse",
            canonical_name="Test Pulse",
            kind=InstrumentKind.PULSE,
            signal_source="test",
        )
    )

    bus = ConstitutionalInstrumentBus(registry=registry)

    observed = []

    bus.subscribe(
        "test.pulse",
        observed.append,
    )

    signal = InstrumentSignal(
        instrument_id="test.pulse",
        signal_type=(InstrumentSignalType.ACTIVITY_STARTED),
        source_identity="test.engine",
        value=1.0,
        status=InstrumentStatus.ACTIVE,
    )

    bus.publish(signal)

    assert observed == [signal]


def test_cognitive_mesh_drives_live_instruments():
    bus, bridge = build_cognition_instrumentation()

    mesh = MultiplicitousIntelligenceMesh(observer=bridge)

    mesh.register(
        participant(
            "knowledge",
            ContributionStance.SUPPORT,
            0.95,
        )
    )

    mesh.register(
        participant(
            "reason",
            ContributionStance.SUPPORT,
            0.90,
        )
    )

    mesh.register(
        participant(
            "risk",
            ContributionStance.CHALLENGE,
            0.30,
        )
    )

    report = mesh.execute(
        assertion_key=ASSERTION,
        payload={
            "card_id": "CARD-001",
        },
    )

    confidence = bus.state("aletheus.instrument.confidence")

    convergence = bus.state("aletheus.instrument.convergence")

    virtue_alignment = bus.state("aletheus.instrument.virtue_alignment")

    truth = bus.state("aletheus.instrument.truth")

    timeline = bus.state("aletheus.instrument.timeline")

    assert confidence.current_value == (report.convergence.confidence)

    assert convergence.current_value == (report.convergence.confidence)

    assert virtue_alignment.current_value == (report.virtues.score)

    assert truth.current_value == 1.0
    assert timeline.update_count > 0


def test_dissent_is_visible_not_hidden():
    bus, bridge = build_cognition_instrumentation()

    mesh = MultiplicitousIntelligenceMesh(observer=bridge)

    mesh.register(
        participant(
            "prediction",
            ContributionStance.SUPPORT,
            0.80,
        )
    )

    mesh.register(
        participant(
            "risk",
            ContributionStance.CHALLENGE,
            0.75,
        )
    )

    report = mesh.execute(
        assertion_key=ASSERTION,
        payload={},
    )

    dissent = bus.state("aletheus.instrument.dissent")

    assert report.convergence.dissent
    assert dissent.current_value > 0
    assert dissent.status == (InstrumentStatus.CONTESTED)


def test_mesh_activity_settles_after_completion():
    bus, bridge = build_cognition_instrumentation()

    mesh = MultiplicitousIntelligenceMesh(observer=bridge)

    mesh.register(
        participant(
            "knowledge",
            ContributionStance.SUPPORT,
            0.90,
        )
    )

    mesh.execute(
        assertion_key=ASSERTION,
        payload={},
    )

    activity = bus.state("aletheus.instrument.mesh_activity")

    assert activity.current_value == 0.0
    assert activity.status == (InstrumentStatus.STABLE)


def test_instrument_snapshot_is_read_only_projection():
    bus, _ = build_cognition_instrumentation()

    snapshot = bus.snapshot()

    assert len(snapshot) == 8

    assert all(state.status == InstrumentStatus.IDLE for state in snapshot.values())
