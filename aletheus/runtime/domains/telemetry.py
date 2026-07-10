class TelemetryDomain:
    def __init__(self, runtime):
        self.runtime = runtime

    def bootstrap(self, payload=None):
        return self.runtime.telemetry_v3.bootstrap()

    def record(self, payload):
        return self.runtime.telemetry_v3.record(
            name=payload.get("name", "runtime.metric"),
            value=payload.get("value"),
            category=payload.get("category", "runtime"),
            metadata=payload.get("metadata", {}),
        )

    def metric(self, payload):
        return self.runtime.telemetry_v3.metric(
            name=payload.get("name", "runtime.metric"),
            value=payload.get("value"),
            category=payload.get("category", "runtime"),
            metadata=payload.get("metadata", {}),
        )

    def log(self, payload):
        return self.runtime.telemetry_v3.log(
            level=payload.get("level", "INFO"),
            message=payload.get("message", ""),
            source=payload.get("source", "runtime"),
            metadata=payload.get("metadata", {}),
        )

    def trace(self, payload):
        return self.runtime.telemetry_v3.trace(
            name=payload.get("name", "runtime.command"),
            status=payload.get("status", "completed"),
            parent_span=payload.get("parent_span"),
            correlation_id=payload.get("correlation_id"),
            metadata=payload.get("metadata", {}),
        )

    def health(self, payload):
        return self.runtime.telemetry_v3.health(
            component=payload.get("component", "runtime"),
            status=payload.get("status", "healthy"),
        )

    def timeline(self, payload):
        return self.runtime.telemetry_v3.timeline(
            message=payload.get("message", ""),
            source=payload.get("source", "runtime"),
            metadata=payload.get("metadata", {}),
        )

    def statistics(self, payload=None):
        return self.runtime.telemetry_v3.statistics()
