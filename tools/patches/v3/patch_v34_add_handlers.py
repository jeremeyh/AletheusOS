from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_federation_bootstrap" in text:
    print("Federation handlers already exist.")
    raise SystemExit(0)

handlers = """

    # ==========================================================
    # v3.4 Federated Knowledge Fabric
    # ==========================================================

    def _cmd_federation_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "federation",
            self.federation_v3.bootstrap(),
        )
        return context

    def _cmd_federation_join(self, context: RuntimeContext) -> RuntimeContext:

        payload = context.payload

        context.add_result(
            "node",
            self.federation_v3.join(
                name=payload.get("name", "Remote Runtime"),
                address=payload.get("address", "localhost"),
                capabilities=payload.get("capabilities", []),
                services=payload.get("services", []),
            ),
        )

        return context

    def _cmd_federation_leave(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "node",
            self.federation_v3.leave(
                context.payload.get("node_id", ""),
            ),
        )

        return context

    def _cmd_federation_discover(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "nodes",
            self.federation_v3.discover(),
        )

        return context

    def _cmd_federation_query(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "federation",
            self.federation_v3.query(),
        )

        return context

    def _cmd_federation_broadcast(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "broadcast",
            self.federation_v3.broadcast(
                context.payload.get("message", ""),
            ),
        )

        return context

    def _cmd_federation_statistics(self, context: RuntimeContext) -> RuntimeContext:

        context.add_result(
            "federation_stats",
            self.federation_v3.statistics(),
        )

        return context

"""

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, handlers + anchor, 1)

core.write_text(text)

print("✔ v3.4 Federation handlers added.")
