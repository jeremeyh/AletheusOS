"""Bridge Constitutional Cognition™ into living instrumentation."""

from __future__ import annotations

from typing import Any

from aletheus.constitutional_cognition import (
    CognitiveSignal,
    CognitiveSignalType,
)

from .bus import ConstitutionalInstrumentBus
from .models import (
    InstrumentSignal,
    InstrumentSignalType,
    InstrumentStatus,
)


class CognitionInstrumentBridge:
    """
    Translate semantic cognitive signals into instrument updates.

    The bridge contains no presentation code. It produces platform-neutral
    instrumentation events that Nimble™ may render in 2D, 3D, voice, spatial,
    or other future experiences.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        bus: ConstitutionalInstrumentBus,
    ) -> None:
        self.bus = bus
        self._translated = 0

    def __call__(
        self,
        signal: CognitiveSignal,
    ) -> None:
        self.project(signal)

    def project(
        self,
        signal: CognitiveSignal,
    ) -> tuple[InstrumentSignal, ...]:
        projected = tuple(self._translate(signal))

        for instrument_signal in projected:
            self.bus.publish(instrument_signal)

        self._translated += len(projected)
        return projected

    def _translate(
        self,
        signal: CognitiveSignal,
    ) -> list[InstrumentSignal]:
        common: dict[str, Any] = {
            "source_identity": (
                signal.engine_id or "aletheus.constitutional_cognition"
            ),
            "cognition_id": signal.cognition_id,
            "message": signal.message,
            "payload": dict(signal.payload),
        }

        timeline = InstrumentSignal(
            instrument_id=("aletheus.instrument.timeline"),
            signal_type=(InstrumentSignalType.TIMELINE_EVENT),
            value=1.0,
            status=self._status_for(signal),
            confidence=signal.magnitude,
            **common,
        )

        projected = [timeline]

        if signal.signal_type == (CognitiveSignalType.MESH_STARTED):
            projected.append(
                InstrumentSignal(
                    instrument_id=("aletheus.instrument.mesh_activity"),
                    signal_type=(InstrumentSignalType.ACTIVITY_STARTED),
                    value=1.0,
                    status=InstrumentStatus.ACTIVE,
                    **common,
                )
            )

        elif signal.signal_type == (CognitiveSignalType.MESH_COMPLETED):
            projected.append(
                InstrumentSignal(
                    instrument_id=("aletheus.instrument.mesh_activity"),
                    signal_type=(InstrumentSignalType.ACTIVITY_COMPLETED),
                    value=0.0,
                    status=InstrumentStatus.STABLE,
                    confidence=signal.magnitude,
                    **{
                        key: value
                        for key, value in common.items()
                        if key != "confidence"
                    },
                )
            )

        elif signal.signal_type == (CognitiveSignalType.ENGINE_STARTED):
            projected.append(
                InstrumentSignal(
                    instrument_id=("aletheus.instrument.engine_activity"),
                    signal_type=(InstrumentSignalType.ACTIVITY_STARTED),
                    value=1.0,
                    status=InstrumentStatus.ACTIVE,
                    **common,
                )
            )

        elif signal.signal_type == (CognitiveSignalType.ENGINE_COMPLETED):
            projected.append(
                InstrumentSignal(
                    instrument_id=("aletheus.instrument.engine_activity"),
                    signal_type=(InstrumentSignalType.VALUE_CHANGED),
                    value=(signal.magnitude if signal.magnitude is not None else 0.0),
                    status=InstrumentStatus.STABLE,
                    confidence=signal.magnitude,
                    **{
                        key: value
                        for key, value in common.items()
                        if key != "confidence"
                    },
                )
            )

        elif signal.signal_type == (CognitiveSignalType.ENGINE_FAILED):
            projected.extend(
                (
                    InstrumentSignal(
                        instrument_id=("aletheus.instrument.engine_activity"),
                        signal_type=(InstrumentSignalType.ACTIVITY_FAILED),
                        value=0.0,
                        status=(InstrumentStatus.DEGRADED),
                        **common,
                    ),
                    InstrumentSignal(
                        instrument_id=("aletheus.instrument.mesh_activity"),
                        signal_type=(InstrumentSignalType.HEALTH_CHANGED),
                        value=0.5,
                        status=(InstrumentStatus.DEGRADED),
                        **common,
                    ),
                )
            )

        elif signal.signal_type == (CognitiveSignalType.CONVERGENCE_COMPLETED):
            confidence = signal.magnitude if signal.magnitude is not None else 0.0

            state = signal.payload.get("state")

            status = (
                InstrumentStatus.CONTESTED
                if state == "contested"
                else InstrumentStatus.STABLE
            )

            dissent_count = int(
                signal.payload.get(
                    "dissent_count",
                    0,
                )
            )

            participant_count = int(
                signal.payload.get(
                    "participant_count",
                    dissent_count + 1,
                )
            )

            dissent_ratio = dissent_count / max(1, participant_count)

            projected.extend(
                (
                    InstrumentSignal(
                        instrument_id=("aletheus.instrument.confidence"),
                        signal_type=(InstrumentSignalType.CONFIDENCE_CHANGED),
                        value=confidence,
                        status=status,
                        confidence=confidence,
                        **{
                            key: value
                            for key, value in common.items()
                            if key != "confidence"
                        },
                    ),
                    InstrumentSignal(
                        instrument_id=("aletheus.instrument.convergence"),
                        signal_type=(InstrumentSignalType.CONVERGENCE_CHANGED),
                        value=confidence,
                        status=status,
                        confidence=confidence,
                        **{
                            key: value
                            for key, value in common.items()
                            if key != "confidence"
                        },
                    ),
                    InstrumentSignal(
                        instrument_id=("aletheus.instrument.dissent"),
                        signal_type=(InstrumentSignalType.DISSENT_CHANGED),
                        value=round(
                            dissent_ratio,
                            4,
                        ),
                        status=(
                            InstrumentStatus.CONTESTED
                            if dissent_count
                            else InstrumentStatus.STABLE
                        ),
                        **common,
                    ),
                )
            )

        elif signal.signal_type == (CognitiveSignalType.VIRTUES_EVALUATED):
            score = signal.magnitude if signal.magnitude is not None else 0.0

            passed = bool(
                signal.payload.get(
                    "passed",
                    False,
                )
            )

            status = InstrumentStatus.STABLE if passed else InstrumentStatus.CAUTION

            violations = set(
                signal.payload.get(
                    "violations",
                    (),
                )
            )

            truth_value = 0.0 if "truth" in violations else 1.0

            projected.extend(
                (
                    InstrumentSignal(
                        instrument_id=("aletheus.instrument.virtue_alignment"),
                        signal_type=(InstrumentSignalType.VIRTUE_STATE_CHANGED),
                        value=score,
                        status=status,
                        confidence=score,
                        **{
                            key: value
                            for key, value in common.items()
                            if key != "confidence"
                        },
                    ),
                    InstrumentSignal(
                        instrument_id=("aletheus.instrument.truth"),
                        signal_type=(InstrumentSignalType.VIRTUE_STATE_CHANGED),
                        value=truth_value,
                        status=(
                            InstrumentStatus.STABLE
                            if truth_value == 1.0
                            else InstrumentStatus.FAILED
                        ),
                        confidence=score,
                        **{
                            key: value
                            for key, value in common.items()
                            if key != "confidence"
                        },
                    ),
                )
            )

        return projected

    @staticmethod
    def _status_for(
        signal: CognitiveSignal,
    ) -> InstrumentStatus:
        if signal.signal_type in {
            CognitiveSignalType.MESH_STARTED,
            CognitiveSignalType.ENGINE_STARTED,
            CognitiveSignalType.CONVERGENCE_STARTED,
        }:
            return InstrumentStatus.ACTIVE

        if signal.signal_type == (CognitiveSignalType.ENGINE_FAILED):
            return InstrumentStatus.DEGRADED

        if (
            signal.signal_type == CognitiveSignalType.CONVERGENCE_COMPLETED
            and signal.payload.get("state") == "contested"
        ):
            return InstrumentStatus.CONTESTED

        return InstrumentStatus.STABLE

    def health(self) -> dict:
        return {
            "name": ("Cognition Instrument Bridge™"),
            "version": self.VERSION,
            "status": "online",
            "translated_signals": (self._translated),
            "instrument_bus": (self.bus.health()),
        }
