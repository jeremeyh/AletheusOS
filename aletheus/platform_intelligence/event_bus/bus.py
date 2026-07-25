"""In-process Constitutional Event Bus."""

from __future__ import annotations

from collections import Counter, deque
from collections.abc import Iterable
from threading import RLock
from types import MappingProxyType
from uuid import UUID

from aletheus.platform_intelligence.events import (
    ConstitutionalEvent,
    ConstitutionalEventKind,
)

from .contracts import (
    ConstitutionalEventHandler,
    ConstitutionalSubscriber,
)
from .exceptions import (
    DuplicateSubscriptionError,
    EventPublicationError,
    SubscriptionNotFoundError,
)
from .statistics import EventBusStatistics
from .subscription import ConstitutionalSubscription


class ConstitutionalEventBus:
    """
    Ordered in-process dispatcher for constitutional facts.

    The bus owns distribution and bounded history only. It does not own
    application state, persistence, networking, retries, or projections.
    """

    def __init__(
        self,
        *,
        history_limit: int = 1000,
        strict_dispatch: bool = False,
    ) -> None:
        if history_limit < 0:
            raise ValueError(
                "history_limit cannot be negative."
            )

        self._history_limit = history_limit
        self._strict_dispatch = strict_dispatch

        self._subscriptions: dict[
            UUID,
            ConstitutionalSubscription,
        ] = {}

        self._history: deque[
            ConstitutionalEvent
        ] = deque(
            maxlen=(
                history_limit
                if history_limit > 0
                else None
            )
        )

        self._published = 0
        self._delivered = 0
        self._failed_deliveries = 0
        self._events_by_kind: Counter[str] = Counter()
        self._next_sequence = 0
        self._last_event: ConstitutionalEvent | None = None

        self._lock = RLock()

    @property
    def history_limit(self) -> int:
        return self._history_limit

    @property
    def strict_dispatch(self) -> bool:
        return self._strict_dispatch

    def subscribe(
        self,
        handler: (
            ConstitutionalEventHandler
            | ConstitutionalSubscriber
        ),
        *,
        kinds: (
            set[ConstitutionalEventKind]
            | frozenset[ConstitutionalEventKind]
            | None
        ) = None,
        source_prefix: str | None = None,
        subject_prefix: str | None = None,
    ) -> UUID:
        resolved_handler = self._resolve_handler(handler)

        subscription = ConstitutionalSubscription.create(
            handler=resolved_handler,
            kinds=kinds,
            source_prefix=source_prefix,
            subject_prefix=subject_prefix,
        )

        with self._lock:
            for current in self._subscriptions.values():
                if (
                    current.handler == subscription.handler
                    and current.kinds == subscription.kinds
                    and current.source_prefix
                    == subscription.source_prefix
                    and current.subject_prefix
                    == subscription.subject_prefix
                ):
                    raise DuplicateSubscriptionError(
                        "An identical subscription already exists."
                    )

            self._subscriptions[
                subscription.subscription_id
            ] = subscription

        return subscription.subscription_id

    def unsubscribe(
        self,
        subscription_id: UUID,
    ) -> None:
        with self._lock:
            if subscription_id not in self._subscriptions:
                raise SubscriptionNotFoundError(
                    f"Subscription not found: "
                    f"{subscription_id}"
                )

            del self._subscriptions[subscription_id]

    def publish(
        self,
        event: ConstitutionalEvent,
    ) -> ConstitutionalEvent:
        with self._lock:
            published_event = event.with_sequence(
                self._next_sequence
            )
            self._next_sequence += 1

            self._published += 1
            self._events_by_kind[
                published_event.kind.value
            ] += 1
            self._last_event = published_event

            if self._history_limit > 0:
                self._history.append(published_event)

            subscriptions = tuple(
                self._subscriptions.values()
            )

        failures: list[Exception] = []

        for subscription in subscriptions:
            if not subscription.matches(published_event):
                continue

            try:
                subscription.handler(published_event)
            except Exception as error:
                with self._lock:
                    self._failed_deliveries += 1

                failures.append(error)

                if self._strict_dispatch:
                    break
            else:
                with self._lock:
                    self._delivered += 1

        if failures and self._strict_dispatch:
            first_error = failures[0]

            raise EventPublicationError(
                "Constitutional event publication failed "
                f"for {published_event.event_id}: "
                f"{type(first_error).__name__}: "
                f"{first_error}"
            ) from first_error

        return published_event

    def publish_batch(
        self,
        events: Iterable[ConstitutionalEvent],
    ) -> tuple[ConstitutionalEvent, ...]:
        return tuple(
            self.publish(event)
            for event in events
        )

    def replay(
        self,
        handler: (
            ConstitutionalEventHandler
            | ConstitutionalSubscriber
        ),
        *,
        kinds: (
            set[ConstitutionalEventKind]
            | frozenset[ConstitutionalEventKind]
            | None
        ) = None,
        source_prefix: str | None = None,
        subject_prefix: str | None = None,
        after_sequence: int | None = None,
    ) -> int:
        resolved_handler = self._resolve_handler(handler)

        subscription = ConstitutionalSubscription.create(
            handler=resolved_handler,
            kinds=kinds,
            source_prefix=source_prefix,
            subject_prefix=subject_prefix,
        )

        with self._lock:
            history = tuple(self._history)

        replayed = 0

        for event in history:
            if (
                after_sequence is not None
                and event.sequence is not None
                and event.sequence <= after_sequence
            ):
                continue

            if not subscription.matches(event):
                continue

            resolved_handler(event)
            replayed += 1

        return replayed

    def history(
        self,
        *,
        kinds: (
            set[ConstitutionalEventKind]
            | frozenset[ConstitutionalEventKind]
            | None
        ) = None,
        after_sequence: int | None = None,
    ) -> tuple[ConstitutionalEvent, ...]:
        with self._lock:
            events = tuple(self._history)

        if not kinds and after_sequence is None:
            return events

        kind_filter = frozenset(kinds or ())

        return tuple(
            event
            for event in events
            if (
                not kind_filter
                or event.kind in kind_filter
            )
            and (
                after_sequence is None
                or event.sequence is None
                or event.sequence > after_sequence
            )
        )

    def clear_history(self) -> None:
        with self._lock:
            self._history.clear()

    def statistics(self) -> EventBusStatistics:
        with self._lock:
            last_event = self._last_event

            return EventBusStatistics(
                published=self._published,
                delivered=self._delivered,
                failed_deliveries=(
                    self._failed_deliveries
                ),
                subscriber_count=len(
                    self._subscriptions
                ),
                history_size=len(self._history),
                next_sequence=self._next_sequence,
                events_by_kind=MappingProxyType(
                    dict(self._events_by_kind)
                ),
                last_event_id=(
                    str(last_event.event_id)
                    if last_event is not None
                    else None
                ),
                last_event_kind=(
                    last_event.kind.value
                    if last_event is not None
                    else None
                ),
            )

    def reset(self) -> None:
        with self._lock:
            self._subscriptions.clear()
            self._history.clear()
            self._published = 0
            self._delivered = 0
            self._failed_deliveries = 0
            self._events_by_kind.clear()
            self._next_sequence = 0
            self._last_event = None

    @staticmethod
    def _resolve_handler(
        handler: (
            ConstitutionalEventHandler
            | ConstitutionalSubscriber
        ),
    ) -> ConstitutionalEventHandler:
        if callable(handler):
            return handler

        object_handler = getattr(
            handler,
            "handle",
            None,
        )

        if callable(object_handler):
            return object_handler

        raise TypeError(
            "Subscriber must be callable or expose "
            "a callable handle(event) method."
        )
