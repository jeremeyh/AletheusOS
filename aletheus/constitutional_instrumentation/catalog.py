"""Canonical Living Constitutional Instrumentation catalog."""

from __future__ import annotations

from .models import (
    InstrumentDefinition,
    InstrumentKind,
)
from .registry import (
    ConstitutionalInstrumentRegistry,
)


def canonical_cognition_instruments() -> tuple[InstrumentDefinition, ...]:
    return (
        InstrumentDefinition(
            instrument_id=("aletheus.instrument.mesh_activity"),
            canonical_name="Mesh Activity Pulse™",
            kind=InstrumentKind.PULSE,
            signal_source=("Multiplicitous Intelligence Mesh™"),
            minimum=0.0,
            maximum=1.0,
            description=(
                "Shows whether constitutional cognition is idle, active, or complete."
            ),
            constitutional_meaning=("Observable cognition lifecycle activity."),
        ),
        InstrumentDefinition(
            instrument_id=("aletheus.instrument.engine_activity"),
            canonical_name="Engine Activity Spectrum™",
            kind=InstrumentKind.SPECTRUM,
            signal_source=("Cognitive participant signals"),
            minimum=0.0,
            maximum=1.0,
            description=(
                "Projects activity and contribution strength across cognitive engines."
            ),
            constitutional_meaning=(
                "Independent engine participation within the intelligence mesh."
            ),
        ),
        InstrumentDefinition(
            instrument_id=("aletheus.instrument.confidence"),
            canonical_name="Constitutional Confidence Dial™",
            kind=InstrumentKind.CONFIDENCE,
            signal_source=("Constitutional Convergence™"),
            minimum=0.0,
            maximum=1.0,
            unit="ratio",
            description=(
                "Shows emergent confidence produced through constitutional convergence."
            ),
            constitutional_meaning=(
                "Confidence derived from independent "
                "engine contributions, not a single model."
            ),
        ),
        InstrumentDefinition(
            instrument_id=("aletheus.instrument.convergence"),
            canonical_name="Convergence Meter™",
            kind=InstrumentKind.CONSENSUS,
            signal_source=("Constitutional Convergence™"),
            minimum=0.0,
            maximum=1.0,
            description=("Shows the degree of directional convergence across engines."),
            constitutional_meaning=(
                "Independent movement toward a shared "
                "conclusion without forced consensus."
            ),
        ),
        InstrumentDefinition(
            instrument_id=("aletheus.instrument.dissent"),
            canonical_name="Dissent Signal™",
            kind=InstrumentKind.METER,
            signal_source=("Constitutional Convergence™"),
            minimum=0.0,
            maximum=1.0,
            description=(
                "Surfaces meaningful directional disagreement between engines."
            ),
            constitutional_meaning=(
                "Preserved dissent and unresolved constitutional tension."
            ),
        ),
        InstrumentDefinition(
            instrument_id=("aletheus.instrument.virtue_alignment"),
            canonical_name="Virtue Alignment Gauge™",
            kind=InstrumentKind.GAUGE,
            signal_source=("Constitutional Virtues Framework™"),
            minimum=0.0,
            maximum=1.0,
            description=(
                "Shows observable alignment with the canonical constitutional virtues."
            ),
            constitutional_meaning=(
                "Truthful, integral, humble, compassionate, "
                "kind, just, wise, and agape-oriented behavior."
            ),
        ),
        InstrumentDefinition(
            instrument_id=("aletheus.instrument.truth"),
            canonical_name="Truth Signal™",
            kind=InstrumentKind.TRUTH,
            signal_source=("Constitutional Virtues Framework™"),
            minimum=0.0,
            maximum=1.0,
            description=(
                "Projects whether cognition remains "
                "evidence-supported and fabrication-free."
            ),
            constitutional_meaning=("Observable constitutional truth alignment."),
        ),
        InstrumentDefinition(
            instrument_id=("aletheus.instrument.timeline"),
            canonical_name="Cognition Timeline™",
            kind=InstrumentKind.TIMELINE,
            signal_source=("Constitutional Cognition™"),
            minimum=0.0,
            maximum=1.0,
            description=("Projects the ordered lifecycle of cognitive activity."),
            constitutional_meaning=(
                "Explainable progression from intent through convergence and virtues."
            ),
        ),
    )


def register_canonical_cognition_instruments(
    registry: ConstitutionalInstrumentRegistry,
) -> ConstitutionalInstrumentRegistry:
    for definition in canonical_cognition_instruments():
        existing = registry.get(definition.instrument_id)

        if existing is None:
            registry.register(definition)
            continue

        if existing != definition:
            raise ValueError(
                f"Conflicting instrument definition for {definition.instrument_id!r}."
            )

    return registry
