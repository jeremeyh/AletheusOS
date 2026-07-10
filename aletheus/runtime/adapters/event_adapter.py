"""
Event Command Adapter

Genesis 7

Extracted from runtime/core.py

Owns EventBus command execution boundary.
"""


class EventCommandAdapter:

    def __init__(self, runtime):
        self.runtime = runtime


    def bootstrap(self, context):

        context.add_result(
            "event_bus",
            self.runtime.event_bus_v3.bootstrap(),
        )

        return context


    def publish(self, context):

        payload = context.payload

        context.add_result(
            "event",
            self.runtime.event_bus_v3.publish(
                topic=payload.get(
                    "topic",
                    "runtime.event",
                ),
                payload=payload.get(
                    "payload",
                    {},
                ),
                publisher=payload.get(
                    "publisher",
                    "runtime",
                ),
                priority=payload.get(
                    "priority",
                    "normal",
                ),
            ),
        )

        return context


    def subscribe(self, context):

        payload = context.payload

        context.add_result(
            "subscription",
            self.runtime.event_bus_v3.subscribe(
                topic=payload.get(
                    "topic",
                    "",
                ),
                subscriber=payload.get(
                    "subscriber",
                    "",
                ),
            ),
        )

        return context


    def unsubscribe(self, context):

        payload = context.payload

        context.add_result(
            "subscription",
            self.runtime.event_bus_v3.unsubscribe(
                topic=payload.get(
                    "topic",
                    "",
                ),
                subscriber=payload.get(
                    "subscriber",
                    "",
                ),
            ),
        )

        return context


    def history(self, context):

        context.add_result(
            "history",
            self.runtime.event_bus_v3.history(
                context.payload.get(
                    "topic"
                )
            ),
        )

        return context


    def replay(self, context):

        context.add_result(
            "replay",
            self.runtime.event_bus_v3.replay(
                context.payload.get(
                    "topic",
                    "",
                )
            ),
        )

        return context


    def statistics(self, context):

        context.add_result(
            "event_stats",
            self.runtime.event_bus_v3.statistics(),
        )

        return context
