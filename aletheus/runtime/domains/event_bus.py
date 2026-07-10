class EventBusDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return self.runtime.event_bus_v3.bootstrap()

    def publish(self, payload):
        return self.runtime.event_bus_v3.publish(
            topic=payload.get("topic", "runtime.event"),
            payload=payload.get("payload", {}),
            publisher=payload.get("publisher", "runtime"),
            priority=payload.get("priority", "normal"),
        )

    def subscribe(self, payload):
        return self.runtime.event_bus_v3.subscribe(
            topic=payload.get("topic", ""),
            subscriber=payload.get("subscriber", ""),
        )

    def unsubscribe(self, payload):
        return self.runtime.event_bus_v3.unsubscribe(
            topic=payload.get("topic", ""),
            subscriber=payload.get("subscriber", ""),
        )

    def history(self, payload):
        return self.runtime.event_bus_v3.history(
            payload.get("topic"),
        )

    def replay(self, payload):
        return self.runtime.event_bus_v3.replay(
            payload.get("topic", ""),
        )

    def statistics(self, payload=None):
        return self.runtime.event_bus_v3.statistics()
