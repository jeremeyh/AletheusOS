from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

if "from aletheus.reasoning import reasoning_core" not in text:
    text = text.replace(
        "from aletheus.knowledge_graph import knowledge_graph_core\n",
        "from aletheus.knowledge_graph import knowledge_graph_core\nfrom aletheus.reasoning import reasoning_core\n",
    )

text = text.replace('self.version = "2.4.0"', 'self.version = "2.5.0"')

if "self.reasoning = reasoning_core" not in text:
    text = text.replace(
        "self.knowledge_graph = knowledge_graph_core\n\n        self.boot()",
        "self.knowledge_graph = knowledge_graph_core\n        self.reasoning = reasoning_core\n\n        self.boot()",
    )

if 'self.commands.register("reason.evaluate"' not in text:
    anchor = '        self.commands.register("knowledge.statistics", self._cmd_kg_statistics)\n'
    insert = '''        self.commands.register("reason.bootstrap", self._cmd_reason_bootstrap)
        self.commands.register("reason.rule.add", self._cmd_reason_rule_add)
        self.commands.register("reason.evaluate", self._cmd_reason_evaluate)
        self.commands.register("reason.explain", self._cmd_reason_explain)
        self.commands.register("reason.trace", self._cmd_reason_trace)
        self.commands.register("reason.decision", self._cmd_reason_decision)
        self.commands.register("reason.confidence", self._cmd_reason_confidence)
        self.commands.register("reason.statistics", self._cmd_reason_statistics)
'''
    if anchor not in text:
        raise SystemExit("Could not find knowledge.statistics command anchor.")
    text = text.replace(anchor, anchor + insert)

if '"Aletheus Cognitive Reasoning Engine"' not in text:
    anchor = '''        self.services.register(
            "Aletheus Knowledge Graph Engine",
            {"status": "online", "version": self.knowledge_graph.version},
        )

        self.scheduler.register(
'''
    replacement = '''        self.services.register(
            "Aletheus Knowledge Graph Engine",
            {"status": "online", "version": self.knowledge_graph.version},
        )
        self.services.register(
            "Aletheus Cognitive Reasoning Engine",
            {"status": "online", "version": self.reasoning.version},
        )

        self.scheduler.register(
'''
    if anchor not in text:
        raise SystemExit("Could not find knowledge graph service anchor.")
    text = text.replace(anchor, replacement)

if '"reasoning_traces": self.reasoning.stats()["traces"]' not in text:
    text = text.replace(
        '''                "graph_nodes": self.knowledge_graph.stats()["nodes"],
                "graph_relationships": self.knowledge_graph.stats()["relationships"],
                "inference_rules": self.knowledge_graph.stats()["inference_rules"],
            },
        )
        return context
''',
        '''                "graph_nodes": self.knowledge_graph.stats()["nodes"],
                "graph_relationships": self.knowledge_graph.stats()["relationships"],
                "inference_rules": self.knowledge_graph.stats()["inference_rules"],
                "reasoning_traces": self.reasoning.stats()["traces"],
                "reasoning_rules": self.reasoning.stats()["rules"],
                "reasoning_confidence": self.reasoning.stats()["confidence"],
            },
        )
        return context
''',
    )

if 'context.add_result("reasoning", self.reasoning.stats())' not in text:
    text = text.replace(
        '''        context.add_result("knowledge_graph", self.knowledge_graph.stats())
        return context
''',
        '''        context.add_result("knowledge_graph", self.knowledge_graph.stats())
        context.add_result("reasoning", self.reasoning.stats())
        return context
''',
    )

if "def _cmd_reason_evaluate" not in text:
    anchor = "    def _job_runtime_pulse(self) -> dict:\n"
    methods = '''
    def _cmd_reason_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("reasoning", self.reasoning.bootstrap_rules())
        return context

    def _cmd_reason_rule_add(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.reasoning.add_rule(
            name=payload.get("name", "Untitled Rule"),
            description=payload.get("description", ""),
            rule_type=payload.get("rule_type", "general"),
            weight=float(payload.get("weight", 0.75)),
        )
        context.add_result("rule", result)
        return context

    def _cmd_reason_evaluate(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.reasoning.evaluate(
            question=payload.get("question", ""),
            runtime=self,
            context=payload.get("context", {}),
        )
        context.add_result("evaluation", result)
        return context

    def _cmd_reason_explain(self, context: RuntimeContext) -> RuntimeContext:
        result = self.reasoning.explain(context.payload.get("trace_id", ""))
        context.add_result("explanation", result)
        return context

    def _cmd_reason_trace(self, context: RuntimeContext) -> RuntimeContext:
        result = self.reasoning.trace(context.payload.get("trace_id", ""))
        context.add_result("trace", result)
        return context

    def _cmd_reason_decision(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.reasoning.decision(
            question=payload.get("question", ""),
            runtime=self,
            context=payload.get("context", {}),
        )
        context.add_result("decision", result)
        return context

    def _cmd_reason_confidence(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("confidence", self.reasoning.confidence())
        return context

    def _cmd_reason_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("reasoning_stats", self.reasoning.stats())
        return context

'''
    if anchor not in text:
        raise SystemExit("Could not find _job_runtime_pulse anchor.")
    text = text.replace(anchor, methods + anchor)

p.write_text(text)
print("v2.5 runtime reasoning engine patch applied.")
