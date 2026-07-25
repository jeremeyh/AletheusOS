from core.event_bus import event_bus
from intelligence.fabric.context import context
from intelligence.fabric.event import Event
from intelligence.journal.event_journal import journal


class Publisher:

    def publish(self,name,payload=None,source="system"):

        event = Event(

            name=name,

            payload=payload or {},

            source=source,

            correlation_id=context.correlation_id,

            causation_id=context.causation_id or ""

        )

        journal.write(

            event.name,

            {

                "event_id":event.event_id,

                "correlation_id":event.correlation_id,

                "causation_id":event.causation_id,

                "timestamp":event.timestamp,

                "source":event.source,

                "payload":event.payload

            }

        )

        print(f"[{event.source}] {event.name}")

        event_bus.publish(

            event.name,

            event.payload

        )


publisher = Publisher()
