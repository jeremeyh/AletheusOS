from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

anchor = 'self.commands.register("cluster.bootstrap", self._cmd_cluster_bootstrap)'

missing = """
        self.commands.register("cluster.join", self._cmd_cluster_join)
        self.commands.register("cluster.leave", self._cmd_cluster_leave)
        self.commands.register("cluster.nodes", self._cmd_cluster_nodes)
        self.commands.register("cluster.services", self._cmd_cluster_services)
        self.commands.register("cluster.heartbeat", self._cmd_cluster_heartbeat)
        self.commands.register("cluster.elect_leader", self._cmd_cluster_elect_leader)
        self.commands.register("cluster.statistics", self._cmd_cluster_statistics)
"""

if 'self.commands.register("cluster.join"' not in text:
    if anchor not in text:
        raise SystemExit("cluster.bootstrap registration not found.")
    text = text.replace(anchor, anchor + "\n" + missing, 1)

if "def _cmd_cluster_join" not in text:
    methods = """
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
        result = self.distributed_v3.leave(context.payload.get("node_id", ""))
        context.add_result("node", result)
        return context

    def _cmd_cluster_nodes(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("nodes", self.distributed_v3.nodes())
        return context

    def _cmd_cluster_services(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("services", self.distributed_v3.services())
        return context

    def _cmd_cluster_heartbeat(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("heartbeat", self.distributed_v3.heartbeat())
        return context

    def _cmd_cluster_elect_leader(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("leader", self.distributed_v3.elect_leader())
        return context

    def _cmd_cluster_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("cluster_stats", self.distributed_v3.statistics())
        return context

"""
    insert_before = "    def _job_runtime_pulse(self) -> dict:"
    if insert_before not in text:
        raise SystemExit("_job_runtime_pulse anchor not found.")
    text = text.replace(insert_before, methods + insert_before, 1)

p.write_text(text)
print("✔ Missing v3.0 cluster commands and handlers registered.")
