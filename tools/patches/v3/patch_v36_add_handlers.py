from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_ha_bootstrap" in text:
    print("HA handlers already exist.")
    raise SystemExit(0)

handlers = '''

    # ==========================================================
    # v3.6 High Availability & Replication
    # ==========================================================

    def _cmd_ha_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("ha", self.high_availability_v3.bootstrap())
        return context

    def _cmd_ha_join(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        context.add_result(
            "node",
            self.high_availability_v3.join(
                name=payload.get("name", "Replica Runtime"),
                metadata=payload.get("metadata", {}),
            ),
        )
        return context

    def _cmd_ha_leave(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "node",
            self.high_availability_v3.leave(context.payload.get("node_id", "")),
        )
        return context

    def _cmd_ha_promote(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "node",
            self.high_availability_v3.promote(context.payload.get("node_id", "")),
        )
        return context

    def _cmd_ha_demote(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "node",
            self.high_availability_v3.demote(context.payload.get("node_id", "")),
        )
        return context

    def _cmd_ha_failover(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("failover", self.high_availability_v3.failover())
        return context

    def _cmd_ha_recover(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "recovery",
            self.high_availability_v3.recover(context.payload.get("node_id", "")),
        )
        return context

    def _cmd_ha_replicate(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "replication",
            self.high_availability_v3.replicate(context.payload.get("payload", {})),
        )
        return context

    def _cmd_ha_status(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("ha_status", self.high_availability_v3.status())
        return context

    def _cmd_ha_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("ha_stats", self.high_availability_v3.statistics())
        return context

'''

anchor = "    def _job_runtime_pulse(self) -> dict:"
if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, handlers + anchor, 1)
core.write_text(text)

print("✔ v3.6 HA handlers added.")
