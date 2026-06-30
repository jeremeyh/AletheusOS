from event_bus.runtime.store import EventStore


class EngineHealthMonitor:
    """
    CardHawkOS Engine Health Monitor™

    Builds health snapshots from recent runtime events.
    """

    @staticmethod
    def snapshot():
        events = EventStore.recent(100)

        failed = [
            event
            for event in events
            if event.get("event_type") == "runtime.step.failed"
        ]

        completed = [
            event
            for event in events
            if event.get("event_type") == "runtime.step.completed"
        ]

        total = len(failed) + len(completed)

        success_rate = 100.0

        if total > 0:
            success_rate = round((len(completed) / total) * 100, 2)

        status = "HEALTHY"

        if failed:
            status = "WARNING"

        if total > 0 and success_rate < 70:
            status = "ERROR"

        return {
            "status": status,
            "events_analyzed": len(events),
            "completed_steps": len(completed),
            "failed_steps": len(failed),
            "success_rate": success_rate,
            "recent_failures": failed[:5],
        }
