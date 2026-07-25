"""Synchronous core of the Constitutional Event Fabric."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from .contracts import ConstitutionalEventSubscriber
from .models import ConstitutionalEvent, ConstitutionalEventType
from .registry import (
    ConstitutionalEventRegistry,
    build_canonical_event_registry,
)

EventHandler = Callable[[ConstitutionalEvent], object]


@dataclass(frozen=True, slots=True)
class EventDelivery:
    event_id: str
    event_type: str
    subscriber_name: str
    delivered: bool
    result: Any = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "subscriber_name": self.subscriber_name,
            "delivered": self.delivered,
            "result": self.result,
            "error": self.error,
        }


@dataclass(slots=True)
class _Subscription:
    subscriber_name: str
    handler: EventHandler


class ConstitutionalEventFabric:
    """
    Typed constitutional event routing and replay.

    This synchronous core provides deterministic behavior for proofs and
    bootstrap. A later adapter can project publication onto the existing
    asynchronous platform Event Bus without changing event contracts.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        registry: ConstitutionalEventRegistry | None = None,
    ) -> None:
        self.registry = registry or build_canonical_event_registry()
        self._subscriptions: dict[
            ConstitutionalEventType,
            list[_Subscription],
        ] = defaultdict(list)
        self._global_subscriptions: list[_Subscription] = []
        self._events: list[ConstitutionalEvent] = []
        self._deliveries: list[EventDelivery] = []

    def subscribe(
        self,
        event_type: ConstitutionalEventType,
        subscriber: ConstitutionalEventSubscriber | EventHandler,
        *,
        subscriber_name: str | None = None,
    ) -> None:
        self.registry.require(event_type)

        handler: EventHandler

        if callable(subscriber):
            handler = subscriber
        elif hasattr(subscriber, "handle"):
            handler = subscriber.handle
        else:
            raise TypeError(
                "Subscriber must be callable or expose handle(event)."
            )

        name = (
            subscriber_name
            or getattr(subscriber, "__name__", None)
            or subscriber.__class__.__name__
        )

        self._subscriptions[event_type].append(
            _Subscription(
                subscriber_name=name,
                handler=handler,
            )
        )

    def subscribe_all(
        self,
        subscriber: ConstitutionalEventSubscriber | EventHandler,
        *,
        subscriber_name: str | None = None,
    ) -> None:
        handler: EventHandler

        if callable(subscriber):
            handler = subscriber
        elif hasattr(subscriber, "handle"):
            handler = subscriber.handle
        else:
            raise TypeError(
                "Subscriber must be callable or expose handle(event)."
            )

        name = (
            subscriber_name
            or getattr(subscriber, "__name__", None)
            or subscriber.__class__.__name__
        )

        self._global_subscriptions.append(
            _Subscription(
                subscriber_name=name,
                handler=handler,
            )
        )

    def publish(
        self,
        event: ConstitutionalEvent,
    ) -> tuple[EventDelivery, ...]:
        definition = self.registry.require(event.event_type)

        if definition.requires_certification and not event.certified:
            raise ValueError(
                f"{event.event_type.value} requires certification."
            )

        self._events.append(event)

        subscriptions = [
            *self._subscriptions[event.event_type],
            *self._global_subscriptions,
        ]

        deliveries = []

        for subscription in subscriptions:
            try:
                result = subscription.handler(event)
                delivery = EventDelivery(
                    event_id=event.event_id,
                    event_type=event.event_type.value,
                    subscriber_name=subscription.subscriber_name,
                    delivered=True,
                    result=result,
                )
            except Exception as exc:
                delivery = EventDelivery(
                    event_id=event.event_id,
                    event_type=event.event_type.value,
                    subscriber_name=subscription.subscriber_name,
                    delivered=False,
                    error=str(exc),
                )

            self._deliveries.append(delivery)
            deliveries.append(delivery)

        return tuple(deliveries)

    def events(
        self,
        *,
        event_type: ConstitutionalEventType | None = None,
        correlation_id: str | None = None,
        source_identity: str | None = None,
    ) -> tuple[ConstitutionalEvent, ...]:
        results = self._events

        if event_type is not None:
            results = [
                event
                for event in results
                if event.event_type == event_type
            ]

        if correlation_id is not None:
            results = [
                event
                for event in results
                if event.correlation_id == correlation_id
            ]

        if source_identity is not None:
            results = [
                event
                for event in results
                if event.source_identity == source_identity
            ]

        return tuple(results)

    def replay(
        self,
        *,
        correlation_id: str | None = None,
        source_identity: str | None = None,
    ) -> tuple[EventDelivery, ...]:
        events = self.events(
            correlation_id=correlation_id,
            source_identity=source_identity,
        )

        deliveries = []

        for event in events:
            subscriptions = [
                *self._subscriptions[event.event_type],
                *self._global_subscriptions,
            ]

            for subscription in subscriptions:
                try:
                    result = subscription.handler(event)
                    delivery = EventDelivery(
                        event_id=event.event_id,
                        event_type=event.event_type.value,
                        subscriber_name=subscription.subscriber_name,
                        delivered=True,
                        result=result,
                    )
                except Exception as exc:
                    delivery = EventDelivery(
                        event_id=event.event_id,
                        event_type=event.event_type.value,
                        subscriber_name=subscription.subscriber_name,
                        delivered=False,
                        error=str(exc),
                    )

                deliveries.append(delivery)
                self._deliveries.append(delivery)

        return tuple(deliveries)

    def deliveries(self) -> tuple[EventDelivery, ...]:
        return tuple(self._deliveries)

    def health(self) -> dict[str, Any]:
        failed_deliveries = sum(
            not delivery.delivered
            for delivery in self._deliveries
        )

        return {
            "name": "Constitutional Event Fabric™",
            "version": self.VERSION,
            "status": "degraded" if failed_deliveries else "online",
            "registered_event_types": (
                self.registry.statistics()["event_types"]
            ),
            "events": len(self._events),
            "subscriptions": (
                sum(len(items) for items in self._subscriptions.values())
                + len(self._global_subscriptions)
            ),
            "deliveries": len(self._deliveries),
            "failed_deliveries": failed_deliveries,
        }
