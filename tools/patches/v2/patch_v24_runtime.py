from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

if "from aletheus.knowledge_graph import knowledge_graph_core" not in text:
    text = text.replace(
        "from aletheus.memory_mesh import memory_mesh_core\n",
        "from aletheus.memory_mesh import memory_mesh_core\nfrom aletheus.knowledge_graph import knowledge_graph_core\n",
    )

text = text.replace('self.version = "2.3.0"', 'self.version = "2.4.0"')

if "self.knowledge_graph = knowledge_graph_core" not in text:
    text = text.replace(
        "self.memory_mesh = memory_mesh_core\n\n        self.boot()",
        "self.memory_mesh = memory_mesh_core\n        self.knowledge_graph = knowledge_graph_core\n\n        self.boot()",
    )

if 'self.commands.register("knowledge.entity.create"' not in text:
    anchor = '        self.commands.register("memory.mesh.stats", self._cmd_memory_mesh_stats)\n'
    insert = '''        self.commands.register("knowledge.entity.create", self._cmd_kg_entity_create)
        self.commands.register("knowledge.entity.update", self._cmd_kg_entity_update)
        self.commands.register("knowledge.entity.delete", self._cmd_kg_entity_delete)
        self.commands.register("knowledge.relationship.create", self._cmd_kg_relationship_create)
        self.commands.register("knowledge.relationship.delete", self._cmd_kg_relationship_delete)
        self.commands.register("knowledge.search", self._cmd_kg_search)
        self.commands.register("knowledge.graph", self._cmd_kg_graph)
        self.commands.register("knowledge.neighbors", self._cmd_kg_neighbors)
        self.commands.register("knowledge.infer", self._cmd_kg_infer)
        self.commands.register("knowledge.bootstrap.cardhawk", self._cmd_kg_bootstrap_cardhawk)
        self.commands.register("knowledge.statistics", self._cmd_kg_statistics)
'''
    if anchor not in text:
        raise SystemExit("Could not find memory.mesh.stats command anchor.")
    text = text.replace(anchor, anchor + insert)

if '"Aletheus Knowledge Graph Engine"' not in text:
    anchor = '''        self.services.register(
            "Aletheus Universal Memory Mesh",
            {"status": "online", "version": self.memory_mesh.version},
        )

        self.scheduler.register(
'''
    replacement = '''        self.services.register(
            "Aletheus Universal Memory Mesh",
            {"status": "online", "version": self.memory_mesh.version},
        )
        self.services.register(
            "Aletheus Knowledge Graph Engine",
            {"status": "online", "version": self.knowledge_graph.version},
        )

        self.scheduler.register(
'''
    if anchor not in text:
        raise SystemExit("Could not find memory mesh service anchor.")
    text = text.replace(anchor, replacement)

if '"graph_nodes": self.knowledge_graph.stats()["nodes"]' not in text:
    text = text.replace(
        '''                "memory_mesh_objects": self.memory_mesh.stats()["memory_objects"],
                "memory_mesh_snapshots": self.memory_mesh.stats()["snapshots"],
                "memory_mesh_versions": self.memory_mesh.stats()["memory_versions"],
            },
        )
        return context
''',
        '''                "memory_mesh_objects": self.memory_mesh.stats()["memory_objects"],
                "memory_mesh_snapshots": self.memory_mesh.stats()["snapshots"],
                "memory_mesh_versions": self.memory_mesh.stats()["memory_versions"],
                "graph_nodes": self.knowledge_graph.stats()["nodes"],
                "graph_relationships": self.knowledge_graph.stats()["relationships"],
                "inference_rules": self.knowledge_graph.stats()["inference_rules"],
            },
        )
        return context
''',
    )

if 'context.add_result("knowledge_graph", self.knowledge_graph.stats())' not in text:
    text = text.replace(
        '''        context.add_result("memory_mesh", self.memory_mesh.stats())
        return context
''',
        '''        context.add_result("memory_mesh", self.memory_mesh.stats())
        context.add_result("knowledge_graph", self.knowledge_graph.stats())
        return context
''',
    )

if "def _cmd_kg_entity_create" not in text:
    anchor = "    def _job_runtime_pulse(self) -> dict:\n"
    methods = '''
    def _cmd_kg_entity_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.knowledge_graph.create_entity(
            name=payload.get("name", "Untitled Entity"),
            node_type=payload.get("node_type", "entity"),
            properties=payload.get("properties", {}),
            metadata=payload.get("metadata", {}),
        )
        context.add_result("entity", result)
        return context

    def _cmd_kg_entity_update(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.knowledge_graph.update_entity(
            node_id=payload.get("node_id", ""),
            properties=payload.get("properties", {}),
            metadata=payload.get("metadata", {}),
        )
        context.add_result("entity", result)
        return context

    def _cmd_kg_entity_delete(self, context: RuntimeContext) -> RuntimeContext:
        result = self.knowledge_graph.delete_entity(context.payload.get("node_id", ""))
        context.add_result("entity", result)
        return context

    def _cmd_kg_relationship_create(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.knowledge_graph.create_relationship(
            source_id=payload.get("source_id", ""),
            target_id=payload.get("target_id", ""),
            relationship_type=payload.get("relationship_type", "related_to"),
            properties=payload.get("properties", {}),
        )
        context.add_result("relationship", result)
        return context

    def _cmd_kg_relationship_delete(self, context: RuntimeContext) -> RuntimeContext:
        result = self.knowledge_graph.delete_relationship(context.payload.get("relationship_id", ""))
        context.add_result("relationship", result)
        return context

    def _cmd_kg_search(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.knowledge_graph.search(
            query=payload.get("query", ""),
            node_type=payload.get("node_type", ""),
        )
        context.add_result("results", result)
        return context

    def _cmd_kg_graph(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("graph", self.knowledge_graph.graph())
        return context

    def _cmd_kg_neighbors(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.knowledge_graph.neighbors(
            node_id=payload.get("node_id", ""),
            direction=payload.get("direction", "both"),
        )
        context.add_result("neighbors", result)
        return context

    def _cmd_kg_infer(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("inference", self.knowledge_graph.infer())
        return context

    def _cmd_kg_bootstrap_cardhawk(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("graph", self.knowledge_graph.bootstrap_cardhawk_graph())
        return context

    def _cmd_kg_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("knowledge_graph_stats", self.knowledge_graph.stats())
        return context

'''
    if anchor not in text:
        raise SystemExit("Could not find _job_runtime_pulse anchor.")
    text = text.replace(anchor, methods + anchor)

p.write_text(text)
print("v2.4 runtime knowledge graph patch applied.")
