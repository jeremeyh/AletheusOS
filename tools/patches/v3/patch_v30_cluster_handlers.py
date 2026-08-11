from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

if "def _cmd_cluster_bootstrap" in text:
    print("Cluster handlers already exist.")
    raise SystemExit(0)

methods = """

    # ============================================================
    # v3.0 Distributed Runtime Fabric
    # ============================================================

    def _cmd_cluster_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "cluster",
            self.distributed_v3.bootstrap(),
        )
        return context

    def _cmd_cluster_join(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload

        result = self.distributed_v3.join(
            node_name=payload.get("node_name", "Unnamed Runtime"),
            capabilities=payload.get("capabilities", []),
            services=payload.get("services", []),
        )

        context.add_result("node", result)
        return context

    def _cmd_cluster_leave(self, context: RuntimeContext) -> RuntimeContext:
        result = self.distributed_v3.leave(
            context.payload.get("node_id", "")
        )

        context.add_result("node", result)
        return context

    def _cmd_cluster_nodes(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "nodes",
            self.distributed_v3.nodes(),
        )
        return context

    def _cmd_cluster_services(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "services",
            self.distributed_v3.services(),
        )
        return context

    def _cmd_cluster_heartbeat(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "heartbeat",
            self.distributed_v3.heartbeat(),
        )
        return context

    def _cmd_cluster_elect_leader(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "leader",
            self.distributed_v3.elect_leader(),
        )
        return context

    def _cmd_cluster_status(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "cluster_status",
            self.distributed_v3.status(),
        )
        return context

    def _cmd_cluster_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(
            "cluster_stats",
            self.distributed_v3.statistics(),
        )
        return context

"""

anchor = "    def _job_runtime_pulse(self) -> dict:"

if anchor not in text:
    raise SystemExit("_job_runtime_pulse anchor not found.")

text = text.replace(anchor, methods + anchor, 1)

core.write_text(text)

print("✔ v3.0 Distributed Runtime handlers added.")
