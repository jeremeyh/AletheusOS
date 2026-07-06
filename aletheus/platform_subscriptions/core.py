from __future__ import annotations

from .registry import SubscriptionRegistry


class PlatformSubscriptionEngine:

    GENESIS = "15.4"
    VERSION = "0.1.0"

    def __init__(self):

        self.registry = SubscriptionRegistry()

    def subscribe(
        self,
        event_type: str,
        subscriber: str,
        callback,
    ):

        return self.registry.register(
            event_type,
            subscriber,
            callback,
        )

    def dispatch(self, event):

        dispatched = 0

        for subscription in self.registry.subscribers(
            event["event_type"]
        ):

            subscription.callback(event)
            dispatched += 1

        return {
            "event": event["event_type"],
            "dispatched": dispatched,
        }

    def health(self):

        return {
            "name": "Platform Subscription Engine",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
            **self.registry.statistics(),
        }

    def statistics(self):

        return self.registry.statistics()


platform_subscriptions = PlatformSubscriptionEngine()
