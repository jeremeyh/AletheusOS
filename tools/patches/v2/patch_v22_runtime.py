from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

if "from aletheus.distributed import distributed_core" not in text:
    text = text.replace(
        "from aletheus.enterprise import enterprise_core\n",
        "from aletheus.enterprise import enterprise_core\nfrom aletheus.distributed import distributed_core\n",
    )

text = text.replace('self.version = "2.1.0"', 'self.version = "2.2.0"')

if "self.distributed = distributed_core" not in text:
    text = text.replace(
        "self.enterprise = enterprise_core\n\n        self.boot()",
        "self.enterprise = enterprise_core\n        self.distributed = distributed_core\n\n        self.boot()",
    )

if 'self.commands.register("cluster.create"' not in text:
    anchor = (
        '        self.commands.register("audit.history", self._cmd_audit_history)\n'
    )
    insert = """        self.commands.register("cluster.create", self._cmd_cluster_create)
        self.commands.register("cluster.bootstrap", self._cmd_cluster_bootstrap)
        self.commands.register("cluster.list", self._cmd_cluster_list)
        self.commands.register("cluster.status", self._cmd_cluster_status)
        self.commands.register("cluster.broadcast", self._cmd_cluster_broadcast)
        self.commands.register("cluster.task.assign", self._cmd_cluster_task_assign)
        self.commands.register("cluster.history", self._cmd_cluster_history)
        self.commands.register("cluster.stats", self._cmd_cluster_stats)
        self.commands.register("node.register", self._cmd_node_register)
        self.commands.register("node.remove", self._cmd_node_remove)
        self.commands.register("node.heartbeat", self._cmd_node_heartbeat)
"""
    if anchor not in text:
        raise SystemExit("Could not find audit.history command anchor.")
    text = text.replace(anchor, anchor + insert)

if '"Aletheus Distributed Intelligence Fabric"' not in text:
    anchor = """        self.services.register(
            "Aletheus Enterprise Intelligence Platform",
            {"status": "online", "version": self.enterprise.version},
        )

        self.scheduler.register(
"""
    replacement = """        self.services.register(
            "Aletheus Enterprise Intelligence Platform",
            {"status": "online", "version": self.enterprise.version},
        )
        self.services.register(
            "Aletheus Distributed Intelligence Fabric",
            {"status": "online", "version": self.distributed.version},
        )

        self.scheduler.register(
"""
    if anchor not in text:
        raise SystemExit("Could not find enterprise service registration anchor.")
    text = text.replace(anchor, replacement)

if '"distributed_clusters": self.distributed.stats()["clusters"]' not in text:
    text = text.replace(
        """                "enterprises": self.enterprise.stats()["organizations"],
                "enterprise_audit_events": self.enterprise.stats()["audit_events"],
                "compliance_score": self.enterprise.stats()["compliance_score"],
            },
        )
        return context
""",
        """                "enterprises": self.enterprise.stats()["organizations"],
                "enterprise_audit_events": self.enterprise.stats()["audit_events"],
                "compliance_score": self.enterprise.stats()["compliance_score"],
                "distributed_clusters": self.distributed.stats()["clusters"],
                "distributed_nodes": self.distributed.stats()["nodes"],
                "distributed_tasks": self.distributed.stats()["tasks"],
            },
        )
        return context
""",
    )

if 'context.add_result("distributed", self.distributed.stats())' not in text:
    text = text.replace(
        """        context.add_result("enterprise", self.enterprise.stats())
        return context
""",
        """        context.add_result("enterprise", self.enterprise.stats())
        context.add_result("distributed", self.distributed.stats())
        return context
""",
    )

if "def _cmd_cluster_create" not in text:
    anchor = "    def _job_runtime_pulse(self) -> dict:\n"
    methods = """
    def _cmd_cluster_create(self, context: RuntimeContext) -> RuntimeContext:
        cluster = self.distributed.create_cluster(
            name=context.payload.get("name", "Aletheus Primary Cluster"),
        )
        self.kernel_v2.publish(
            event_type="cluster.created",
            source="distributed_fabric",
            payload=cluster.to_dict(),
        )
        context.add_result("cluster", cluster.to_dict())
        return context

    def _cmd_cluster_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        cluster = self.distributed.bootstrap_primary_cluster()
        self.kernel_v2.publish(
            event_type="cluster.bootstrapped",
            source="distributed_fabric",
            payload=cluster.to_dict(),
        )
        context.add_result("cluster", cluster.to_dict())
        return context

    def _cmd_cluster_list(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("clusters", self.distributed.list_clusters())
        return context

    def _cmd_cluster_status(self, context: RuntimeContext) -> RuntimeContext:
        result = self.distributed.cluster_status(context.payload.get("cluster_id", ""))
        context.add_result("cluster_status", result)
        return context

    def _cmd_cluster_broadcast(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.distributed.broadcast(
            cluster_id=payload.get("cluster_id", ""),
            message=payload.get("message", ""),
            payload=payload.get("payload", {}),
        )
        context.add_result("broadcast", result)
        return context

    def _cmd_cluster_task_assign(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.distributed.assign_task(
            cluster_id=payload.get("cluster_id", ""),
            title=payload.get("title", "Untitled Distributed Task"),
            objective=payload.get("objective", ""),
            capability=payload.get("capability", ""),
        )
        context.add_result("task", result)
        return context

    def _cmd_cluster_history(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("history", self.distributed.history())
        return context

    def _cmd_cluster_stats(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("cluster_stats", self.distributed.stats())
        return context

    def _cmd_node_register(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.distributed.register_node(
            cluster_id=payload.get("cluster_id", ""),
            name=payload.get("name", "Unnamed Node"),
            node_type=payload.get("node_type", "runtime"),
            capabilities=payload.get("capabilities", []),
            address=payload.get("address", "local"),
            metadata=payload.get("metadata", {}),
        )
        context.add_result("node", result)
        return context

    def _cmd_node_remove(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.distributed.remove_node(
            cluster_id=payload.get("cluster_id", ""),
            node_id=payload.get("node_id", ""),
        )
        context.add_result("node", result)
        return context

    def _cmd_node_heartbeat(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.distributed.heartbeat(
            cluster_id=payload.get("cluster_id", ""),
            node_id=payload.get("node_id", ""),
        )
        context.add_result("heartbeat", result)
        return context

"""
    if anchor not in text:
        raise SystemExit("Could not find _job_runtime_pulse anchor.")
    text = text.replace(anchor, methods + anchor)

p.write_text(text)
print("v2.2 runtime distributed fabric patch applied.")
