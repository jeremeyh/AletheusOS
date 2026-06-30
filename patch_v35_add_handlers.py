from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_telemetry_bootstrap" in text:
    print("Telemetry handlers already exist.")
    raise SystemExit(0)

handlers = '''

    # ==========================================================
    # v3.5 Observability & Telemetry Platform
    # ==========================================================

    def _cmd_telemetry_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "telemetry",
            self.telemetry_v3.bootstrap(),
        )
        return context

    def _cmd_telemetry_record(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "record",
            self.telemetry_v3.record(
                name=payload.get("name", "runtime.metric"),
                value=payload.get("value"),
                category=payload.get("category", "runtime"),
                metadata=payload.get("metadata", {}),
            ),
        )

        return context

    def _cmd_telemetry_metric(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "metric",
            self.telemetry_v3.metric(
                name=payload.get("name", "runtime.metric"),
                value=payload.get("value"),
                category=payload.get("category", "runtime"),
                metadata=payload.get("metadata", {}),
            ),
        )

        return context

    def _cmd_telemetry_log(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "log",
            self.telemetry_v3.log(
                level=payload.get("level", "INFO"),
                message=payload.get("message", ""),
                source=payload.get("source", "runtime"),
                metadata=payload.get("metadata", {}),
            ),
        )

        return context

    def _cmd_telemetry_trace(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "trace",
            self.telemetry_v3.trace(
                name=payload.get("name", "runtime.command"),
                status=payload.get("status", "completed"),
                parent_span=payload.get("parent_span"),
                correlation_id=payload.get("correlation_id"),
                metadata=payload.get("metadata", {}),
            ),
        )

        return context

    def _cmd_telemetry_health(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "health",
            self.telemetry_v3.health(
                component=payload.get("component", "runtime"),
                status=payload.get("status", "healthy"),
            ),
        )

        return context

    def _cmd_telemetry_timeline(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "timeline",
            self.telemetry_v3.timeline(
                message=payload.get("message", ""),
                source=payload.get("source", "runtime"),
                metadata=payload.get("metadata", {}),
            ),
        )

        return context

    def _cmd_telemetry_statistics(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "telemetry_stats",
            self.telemetry_v3.statistics(),
        )

        return context

'''

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, handlers + anchor, 1)

core.write_text(text)

print("✔ v3.5 Telemetry handlers added.")
