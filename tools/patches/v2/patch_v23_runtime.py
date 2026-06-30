from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

if "from aletheus.memory_mesh import memory_mesh_core" not in text:
    text = text.replace(
        "from aletheus.distributed import distributed_core\n",
        "from aletheus.distributed import distributed_core\nfrom aletheus.memory_mesh import memory_mesh_core\n",
    )

text = text.replace('self.version = "2.2.0"', 'self.version = "2.3.0"')

if "self.memory_mesh = memory_mesh_core" not in text:
    text = text.replace(
        "self.distributed = distributed_core\n\n        self.boot()",
        "self.distributed = distributed_core\n        self.memory_mesh = memory_mesh_core\n\n        self.boot()",
    )

if 'self.commands.register("memory.mesh.store"' not in text:
    anchor = '        self.commands.register("node.heartbeat", self._cmd_node_heartbeat)\n'
    insert = '''        self.commands.register("memory.mesh.store", self._cmd_memory_mesh_store)
        self.commands.register("memory.mesh.retrieve", self._cmd_memory_mesh_retrieve)
        self.commands.register("memory.mesh.search", self._cmd_memory_mesh_search)
        self.commands.register("memory.mesh.snapshot", self._cmd_memory_mesh_snapshot)
        self.commands.register("memory.mesh.restore", self._cmd_memory_mesh_restore)
        self.commands.register("memory.mesh.replicate", self._cmd_memory_mesh_replicate)
        self.commands.register("memory.mesh.sync", self._cmd_memory_mesh_sync)
        self.commands.register("memory.mesh.history", self._cmd_memory_mesh_history)
        self.commands.register("memory.mesh.cache", self._cmd_memory_mesh_cache)
        self.commands.register("memory.mesh.stats", self._cmd_memory_mesh_stats)
'''
    if anchor not in text:
        raise SystemExit("Could not find node.heartbeat command anchor.")
    text = text.replace(anchor, anchor + insert)

if '"Aletheus Universal Memory Mesh"' not in text:
    anchor = '''        self.services.register(
            "Aletheus Distributed Intelligence Fabric",
            {"status": "online", "version": self.distributed.version},
        )

        self.scheduler.register(
'''
    replacement = '''        self.services.register(
            "Aletheus Distributed Intelligence Fabric",
            {"status": "online", "version": self.distributed.version},
        )
        self.services.register(
            "Aletheus Universal Memory Mesh",
            {"status": "online", "version": self.memory_mesh.version},
        )

        self.scheduler.register(
'''
    if anchor not in text:
        raise SystemExit("Could not find distributed service registration anchor.")
    text = text.replace(anchor, replacement)

if '"memory_mesh_objects": self.memory_mesh.stats()["memory_objects"]' not in text:
    text = text.replace(
        '''                "distributed_clusters": self.distributed.stats()["clusters"],
                "distributed_nodes": self.distributed.stats()["nodes"],
                "distributed_tasks": self.distributed.stats()["tasks"],
            },
        )
        return context
''',
        '''                "distributed_clusters": self.distributed.stats()["clusters"],
                "distributed_nodes": self.distributed.stats()["nodes"],
                "distributed_tasks": self.distributed.stats()["tasks"],
                "memory_mesh_objects": self.memory_mesh.stats()["memory_objects"],
                "memory_mesh_snapshots": self.memory_mesh.stats()["snapshots"],
                "memory_mesh_versions": self.memory_mesh.stats()["memory_versions"],
            },
        )
        return context
''',
    )

if 'context.add_result("memory_mesh", self.memory_mesh.stats())' not in text:
    text = text.replace(
        '''        context.add_result("distributed", self.distributed.stats())
        return context
''',
        '''        context.add_result("distributed", self.distributed.stats())
        context.add_result("memory_mesh", self.memory_mesh.stats())
        return context
''',
    )

if "def _cmd_memory_mesh_store" not in text:
    anchor = "    def _job_runtime_pulse(self) -> dict:\n"
    methods = '''
    def _cmd_memory_mesh_store(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.memory_mesh.store(
            key=payload.get("key", "untitled"),
            value=payload.get("value"),
            namespace=payload.get("namespace", "global"),
            object_type=payload.get("object_type", "generic"),
            tags=payload.get("tags", []),
            owner=payload.get("owner", context.application),
            metadata=payload.get("metadata", {}),
        )
        context.add_result("memory_object", result)
        return context

    def _cmd_memory_mesh_retrieve(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.memory_mesh.retrieve(
            object_id=payload.get("object_id", ""),
            key=payload.get("key", ""),
            namespace=payload.get("namespace", "global"),
        )
        context.add_result("memory_object", result)
        return context

    def _cmd_memory_mesh_search(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.memory_mesh.search(
            query=payload.get("query", ""),
            tags=payload.get("tags", []),
            namespace=payload.get("namespace", ""),
        )
        context.add_result("results", result)
        return context

    def _cmd_memory_mesh_snapshot(self, context: RuntimeContext) -> RuntimeContext:
        result = self.memory_mesh.snapshot(context.payload.get("name", "Memory Mesh Snapshot"))
        context.add_result("snapshot", result)
        return context

    def _cmd_memory_mesh_restore(self, context: RuntimeContext) -> RuntimeContext:
        result = self.memory_mesh.restore(context.payload.get("snapshot_id", ""))
        context.add_result("restore", result)
        return context

    def _cmd_memory_mesh_replicate(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.memory_mesh.replicate(
            object_id=payload.get("object_id", ""),
            target_node=payload.get("target_node", "primary"),
        )
        context.add_result("replication", result)
        return context

    def _cmd_memory_mesh_sync(self, context: RuntimeContext) -> RuntimeContext:
        result = self.memory_mesh.sync(context.payload.get("node", "distributed_fabric"))
        context.add_result("sync", result)
        return context

    def _cmd_memory_mesh_history(self, context: RuntimeContext) -> RuntimeContext:
        result = self.memory_mesh.history(context.payload.get("object_id", ""))
        context.add_result("history", result)
        return context

    def _cmd_memory_mesh_cache(self, context: RuntimeContext) -> RuntimeContext:
        result = self.memory_mesh.cache(context.payload.get("object_id", ""))
        context.add_result("cache", result)
        return context

    def _cmd_memory_mesh_stats(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("memory_mesh_stats", self.memory_mesh.stats())
        return context

'''
    if anchor not in text:
        raise SystemExit("Could not find _job_runtime_pulse anchor.")
    text = text.replace(anchor, methods + anchor)

p.write_text(text)
print("v2.3 runtime memory mesh patch applied.")
