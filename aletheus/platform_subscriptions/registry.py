from __future__ import annotations

from .models import Subscription


class SubscriptionRegistry:

    def __init__(self):
        self._subscriptions: list[Subscription] = []

    def register(
        self,
        event_type: str,
        subscriber: str,
        callback,
    ):

        subscription = Subscription(
            event_type=event_type,
            subscriber=subscriber,
            callback=callback,
        )

        self._subscriptions.append(subscription)

        return subscription

    def subscribers(self, event_type: str):

        return [
            s
            for s in self._subscriptions
            if s.event_type == event_type
        ]

    def statistics(self):

        return {
            "subscriptions": len(self._subscriptions),
        }
