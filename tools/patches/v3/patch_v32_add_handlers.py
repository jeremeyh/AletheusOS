from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_state_bootstrap" in text:
    print("Persistence handlers already exist.")
    raise SystemExit(0)

handlers = """

    # ==========================================================
    # v3.2 Persistence Engine
    # ==========================================================

    def _cmd_state_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "state",
            self.persistence_v3.bootstrap(),
        )
        return context

    def _cmd_state_save(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "state",
            self.persistence_v3.save(self),
        )
        return context

    def _cmd_state_load(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "state",
            self.persistence_v3.load(),
        )
        return context

    def _cmd_state_snapshot(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "snapshot",
            self.persistence_v3.snapshot(
                name=context.payload.get("name", "Runtime Snapshot"),
                runtime=self,
            ),
        )
        return context

    def _cmd_state_restore(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "state",
            self.persistence_v3.restore(
                context.payload.get("snapshot_id", "")
            ),
        )
        return context

    def _cmd_state_export(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "state",
            self.persistence_v3.export(),
        )
        return context

    def _cmd_state_import(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "state",
            self.persistence_v3.import_state(
                context.payload.get("state", {})
            ),
        )
        return context

    def _cmd_state_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "state_stats",
            self.persistence_v3.statistics(),
        )
        return context

"""

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, handlers + anchor, 1)

core.write_text(text)

print("✔ v3.2 Persistence Engine handlers added.")
