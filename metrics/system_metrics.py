from observability.telemetry import Telemetry
class SystemMetrics:
    @staticmethod
    def snapshot():
        Telemetry.record("system.online",1)
        return {
            "cpu":"N/A",
            "memory":"N/A",
            "queue_depth":0,
            "telemetry_events":len(Telemetry.latest())
        }
