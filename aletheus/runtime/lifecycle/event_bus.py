from .events import RuntimeLifecycleEvent


class RuntimeLifecycleEventBus:
    """
    Runtime Lifecycle Event Bus™

    Publishes lifecycle events to interested runtime components.
    """

    def __init__(self):

        self._events = []

    def publish(self, state):

        event = RuntimeLifecycleEvent(state=state)

        self._events.append(event)

        return event

    @property
    def events(self):

        return tuple(self._events)

    def clear(self):

        self._events.clear()
