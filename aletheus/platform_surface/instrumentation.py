"""Public Living Constitutional Instrumentation Surface."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aletheus.constitutional_instrumentation import (
    ConstitutionalInstrumentBus,
    InstrumentSignal,
    InstrumentState,
)

InstrumentObserver = Callable[
    [InstrumentSignal],
    None,
]


class InstrumentationSurface:
    """
    Stable application-facing instrumentation interface.

    Applications consume semantic instrument state rather than reaching into
    the Instrument Bus or cognitive engines directly.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        bus: ConstitutionalInstrumentBus,
    ) -> None:
        self._bus = bus

    def state(
        self,
        instrument_id: str,
    ) -> InstrumentState:
        return self._bus.state(instrument_id)

    def signals(
        self,
        instrument_id: str,
    ) -> tuple[InstrumentSignal, ...]:
        return self._bus.signals(instrument_id)

    def snapshot(
        self,
    ) -> dict[str, InstrumentState]:
        return self._bus.snapshot()

    def subscribe(
        self,
        instrument_id: str,
        observer: InstrumentObserver,
    ) -> None:
        self._bus.subscribe(
            instrument_id,
            observer,
        )

    def subscribe_all(
        self,
        observer: InstrumentObserver,
    ) -> None:
        self._bus.subscribe_all(observer)

    def statistics(self) -> dict[str, Any]:
        return self._bus.statistics()

    def health(self) -> dict[str, Any]:
        return self._bus.health()
