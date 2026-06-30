from event_bus.runtime.store import EventStore


class EventBus:
    _subscribers = {}

    @classmethod
    def subscribe(cls, event_type, callback):
        if event_type not in cls._subscribers:
            cls._subscribers[event_type] = []

        cls._subscribers[event_type].append(callback)

    @classmethod
    def publish(
        cls,
        event_type,
        payload=None,
        source="CardHawkOS",
        asset_id=None,
        title="",
        message="",
    ):
        payload = payload or {}

        EventStore.record(
            event_type=event_type,
            source=source,
            asset_id=asset_id,
            title=title,
            message=message,
            payload=str(payload),
        )

        for callback in cls._subscribers.get(event_type, []):
            callback(payload)

        return {
            "event_type": event_type,
            "source": source,
            "asset_id": asset_id,
            "title": title,
            "message": message,
            "payload": payload,
        }
