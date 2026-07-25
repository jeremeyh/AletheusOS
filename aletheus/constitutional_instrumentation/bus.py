"""Constitutional Instrument Bus™."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from typing import Any

from .models import (
    InstrumentSignal,
    InstrumentState,
    InstrumentStatus,
)
from .registry import (
    ConstitutionalInstrumentRegistry,
)

InstrumentSubscriber = Callable[
    [InstrumentSignal],
    None,
]


class ConstitutionalInstrumentBus:
    """
    Publish semantically meaningful instrument signals and project state.

    The bus is intentionally distinct from the Constitutional Event Fabric:

    - Event Fabric records authoritative constitutional events.
    - Instrument Bus projects rapidly changing observable telemetry.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        registry: (
            ConstitutionalInstrumentRegistry
            | None
        ) = None,
        history_limit: int = 100,
    ) -> None:
        if history_limit < 1:
            raise ValueError(
                "history_limit must be at least one."
            )

        self.registry = (
            registry
            or ConstitutionalInstrumentRegistry()
        )

        self.history_limit = history_limit

        self._signals: dict[
            str,
            list[InstrumentSignal],
        ] = defaultdict(list)

        self._subscribers: dict[
            str,
            list[InstrumentSubscriber],
        ] = defaultdict(list)

        self._all_subscribers: list[
            InstrumentSubscriber
        ] = []

        self._published = 0
        self._subscriber_failures = 0

    def subscribe(
        self,
        instrument_id: str,
        subscriber: InstrumentSubscriber,
    ) -> None:
        self.registry.require(
            instrument_id
        )

        if subscriber not in self._subscribers[
            instrument_id
        ]:
            self._subscribers[
                instrument_id
            ].append(subscriber)

    def subscribe_all(
        self,
        subscriber: InstrumentSubscriber,
    ) -> None:
        if subscriber not in self._all_subscribers:
            self._all_subscribers.append(
                subscriber
            )

    def publish(
        self,
        signal: InstrumentSignal,
    ) -> InstrumentSignal:
        definition = self.registry.require(
            signal.instrument_id
        )

        if signal.value is not None:
            if not (
                definition.minimum
                <= signal.value
                <= definition.maximum
            ):
                raise ValueError(
                    f"Signal value {signal.value!r} "
                    f"is outside the range for "
                    f"{signal.instrument_id!r}."
                )

        history = self._signals[
            signal.instrument_id
        ]

        history.append(signal)

        if len(history) > self.history_limit:
            del history[
                : len(history)
                - self.history_limit
            ]

        subscribers = [
            *self._subscribers[
                signal.instrument_id
            ],
            *self._all_subscribers,
        ]

        for subscriber in subscribers:
            try:
                subscriber(signal)
            except Exception:
                self._subscriber_failures += 1

        self._published += 1
        return signal

    def signals(
        self,
        instrument_id: str,
    ) -> tuple[InstrumentSignal, ...]:
        self.registry.require(
            instrument_id
        )

        return tuple(
            self._signals.get(
                instrument_id,
                (),
            )
        )

    def state(
        self,
        instrument_id: str,
    ) -> InstrumentState:
        definition = self.registry.require(
            instrument_id
        )

        history = self.signals(
            instrument_id
        )

        latest = (
            history[-1]
            if history
            else None
        )

        return InstrumentState(
            instrument_id=(
                definition.instrument_id
            ),
            canonical_name=(
                definition.canonical_name
            ),
            kind=definition.kind,
            current_value=(
                latest.value
                if latest
                else None
            ),
            minimum=definition.minimum,
            maximum=definition.maximum,
            unit=definition.unit,
            status=(
                latest.status
                if (
                    latest
                    and latest.status
                    is not None
                )
                else InstrumentStatus.IDLE
            ),
            confidence=(
                latest.confidence
                if latest
                else None
            ),
            update_count=len(history),
            last_signal_id=(
                latest.signal_id
                if latest
                else None
            ),
            last_updated=(
                latest.emitted_at
                if latest
                else None
            ),
            last_message=(
                latest.message
                if latest
                else ""
            ),
            history=history,
            metadata=dict(
                definition.metadata
            ),
        )

    def snapshot(
        self,
    ) -> dict[str, InstrumentState]:
        return {
            definition.instrument_id: (
                self.state(
                    definition.instrument_id
                )
            )
            for definition
            in self.registry.list()
        }

    def statistics(self) -> dict[str, Any]:
        return {
            "published_signals": (
                self._published
            ),
            "subscriber_failures": (
                self._subscriber_failures
            ),
            "instrument_subscriptions": sum(
                len(subscribers)
                for subscribers
                in self._subscribers.values()
            ),
            "global_subscriptions": len(
                self._all_subscribers
            ),
            "instruments_with_history": sum(
                bool(signals)
                for signals
                in self._signals.values()
            ),
        }

    def health(self) -> dict[str, Any]:
        return {
            "name": (
                "Constitutional Instrument Bus™"
            ),
            "version": self.VERSION,
            "status": (
                "degraded"
                if self._subscriber_failures
                else "online"
            ),
            "registry": self.registry.health(),
            **self.statistics(),
        }
