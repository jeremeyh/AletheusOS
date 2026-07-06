from __future__ import annotations

from aletheus.platform_subscriptions import platform_subscriptions

from .core import platform_timeline


class TimelineSubscriber:
    """
    Automatically records every platform event
    into the Platform Timeline.
    """

    NAME = "Platform Timeline Subscriber"

    def handle(self, event):

        platform_timeline.record(
            event_type=event["event_type"],
            source=event["source"],
            message=event["event_type"],
            payload=event.get("payload", {}),
        )

    def register(self):

        platform_subscriptions.subscribe(
            "platform.starting",
            self.NAME,
            self.handle,
        )

        platform_subscriptions.subscribe(
            "platform.online",
            self.NAME,
            self.handle,
        )

        platform_subscriptions.subscribe(
            "platform.shutdown",
            self.NAME,
            self.handle,
        )

        platform_subscriptions.subscribe(
            "platform.degraded",
            self.NAME,
            self.handle,
        )

        return True


timeline_subscriber = TimelineSubscriber()
