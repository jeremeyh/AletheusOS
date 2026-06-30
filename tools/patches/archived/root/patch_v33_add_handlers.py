from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_event_bootstrap" in text:
    print("Event Bus handlers already exist.")
    raise SystemExit(0)

handlers = '''

    # ==========================================================
    # v3.3 Event Streaming & Message Bus
    # ==========================================================

    def _cmd_event_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "event_bus",
            self.event_bus_v3.bootstrap(),
        )
        return context

    def _cmd_event_publish(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "event",
            self.event_bus_v3.publish(
                topic=payload.get("topic", "runtime.event"),
                payload=payload.get("payload", {}),
                publisher=payload.get("publisher", "runtime"),
                priority=payload.get("priority", "normal"),
            ),
        )

        return context

    def _cmd_event_subscribe(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "subscription",
            self.event_bus_v3.subscribe(
                topic=payload.get("topic", ""),
                subscriber=payload.get("subscriber", ""),
            ),
        )

        return context

    def _cmd_event_unsubscribe(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "subscription",
            self.event_bus_v3.unsubscribe(
                topic=payload.get("topic", ""),
                subscriber=payload.get("subscriber", ""),
            ),
        )

        return context

    def _cmd_event_history(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "history",
            self.event_bus_v3.history(
                context.payload.get("topic"),
            ),
        )

        return context

    def _cmd_event_replay(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "replay",
            self.event_bus_v3.replay(
                context.payload.get("topic", ""),
            ),
        )

        return context

    def _cmd_event_statistics(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "event_stats",
            self.event_bus_v3.statistics(),
        )

        return context

'''

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, handlers + anchor, 1)

core.write_text(text)

print("✔ v3.3 Event Bus handlers added.")
