"""Instrumentation projections for Constitutional Scenarios™."""

from __future__ import annotations

from aletheus.constitutional_instrumentation import (
    ConstitutionalInstrumentBus,
    InstrumentDefinition,
    InstrumentKind,
    InstrumentSignal,
    InstrumentSignalType,
    InstrumentStatus,
)

from .models import ScenarioOutcome


SCENARIO_CONFIDENCE_ID = (
    "aletheus.instrument.scenario_confidence"
)

SCENARIO_VIRTUE_ID = (
    "aletheus.instrument.scenario_virtue_alignment"
)

SCENARIO_ACTIVITY_ID = (
    "aletheus.instrument.scenario_activity"
)


def register_scenario_instruments(
    bus: ConstitutionalInstrumentBus,
) -> ConstitutionalInstrumentBus:
    definitions = (
        InstrumentDefinition(
            instrument_id=(
                SCENARIO_ACTIVITY_ID
            ),
            canonical_name=(
                "Scenario Activity Pulse™"
            ),
            kind=InstrumentKind.PULSE,
            signal_source=(
                "Constitutional Scenario Engine™"
            ),
            minimum=0.0,
            maximum=1.0,
            constitutional_meaning=(
                "Live scenario evaluation activity."
            ),
        ),
        InstrumentDefinition(
            instrument_id=(
                SCENARIO_CONFIDENCE_ID
            ),
            canonical_name=(
                "Scenario Confidence Dial™"
            ),
            kind=InstrumentKind.CONFIDENCE,
            signal_source=(
                "Constitutional Scenario Engine™"
            ),
            minimum=0.0,
            maximum=1.0,
            constitutional_meaning=(
                "Emergent confidence for one "
                "explicit hypothetical branch."
            ),
        ),
        InstrumentDefinition(
            instrument_id=(
                SCENARIO_VIRTUE_ID
            ),
            canonical_name=(
                "Scenario Virtue Alignment Gauge™"
            ),
            kind=InstrumentKind.GAUGE,
            signal_source=(
                "Constitutional Scenario Engine™"
            ),
            minimum=0.0,
            maximum=1.0,
            constitutional_meaning=(
                "Constitutional alignment of the "
                "scenario evaluation."
            ),
        ),
    )

    for definition in definitions:
        existing = bus.registry.get(
            definition.instrument_id
        )

        if existing is None:
            bus.registry.register(
                definition
            )
        elif existing != definition:
            raise ValueError(
                "Conflicting scenario instrument "
                f"{definition.instrument_id!r}."
            )

    return bus


class ScenarioInstrumentPublisher:
    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        bus: ConstitutionalInstrumentBus,
    ) -> None:
        self.bus = register_scenario_instruments(
            bus
        )

        self._published = 0

    def started(
        self,
        *,
        scenario_id: str,
        run_id: str,
    ) -> None:
        self.bus.publish(
            InstrumentSignal(
                instrument_id=(
                    SCENARIO_ACTIVITY_ID
                ),
                signal_type=(
                    InstrumentSignalType
                    .ACTIVITY_STARTED
                ),
                source_identity=(
                    "aletheus.constitutional_scenarios"
                ),
                value=1.0,
                status=InstrumentStatus.ACTIVE,
                correlation_id=run_id,
                message=(
                    f"Scenario {scenario_id} "
                    "evaluation started."
                ),
                payload={
                    "scenario_id": scenario_id,
                    "run_id": run_id,
                },
            )
        )

        self._published += 1

    def completed(
        self,
        outcome: ScenarioOutcome,
    ) -> None:
        status = (
            InstrumentStatus.CONTESTED
            if outcome.status.value
            == "contested"
            else InstrumentStatus.STABLE
        )

        signals = (
            InstrumentSignal(
                instrument_id=(
                    SCENARIO_CONFIDENCE_ID
                ),
                signal_type=(
                    InstrumentSignalType
                    .CONFIDENCE_CHANGED
                ),
                source_identity=(
                    "aletheus.constitutional_scenarios"
                ),
                value=outcome.confidence,
                confidence=outcome.confidence,
                status=status,
                correlation_id=outcome.run_id,
                message=(
                    "Scenario confidence updated."
                ),
                payload={
                    "scenario_id": (
                        outcome.scenario_id
                    ),
                    "run_id": outcome.run_id,
                },
            ),
            InstrumentSignal(
                instrument_id=(
                    SCENARIO_VIRTUE_ID
                ),
                signal_type=(
                    InstrumentSignalType
                    .VIRTUE_STATE_CHANGED
                ),
                source_identity=(
                    "aletheus.constitutional_scenarios"
                ),
                value=outcome.virtue_score,
                confidence=outcome.virtue_score,
                status=(
                    InstrumentStatus.STABLE
                    if outcome.report.virtues.passed
                    else InstrumentStatus.CAUTION
                ),
                correlation_id=outcome.run_id,
                message=(
                    "Scenario virtue alignment updated."
                ),
                payload={
                    "scenario_id": (
                        outcome.scenario_id
                    ),
                    "run_id": outcome.run_id,
                },
            ),
            InstrumentSignal(
                instrument_id=(
                    SCENARIO_ACTIVITY_ID
                ),
                signal_type=(
                    InstrumentSignalType
                    .ACTIVITY_COMPLETED
                ),
                source_identity=(
                    "aletheus.constitutional_scenarios"
                ),
                value=0.0,
                status=InstrumentStatus.STABLE,
                correlation_id=outcome.run_id,
                message=(
                    "Scenario evaluation completed."
                ),
                payload={
                    "scenario_id": (
                        outcome.scenario_id
                    ),
                    "run_id": outcome.run_id,
                },
            ),
        )

        for signal in signals:
            self.bus.publish(signal)

        self._published += len(signals)

    def health(self) -> dict:
        return {
            "name": (
                "Scenario Instrument Publisher™"
            ),
            "version": self.VERSION,
            "status": "online",
            "published_signals": (
                self._published
            ),
        }
