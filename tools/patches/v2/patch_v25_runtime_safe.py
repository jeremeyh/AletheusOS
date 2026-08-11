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
        "self.knowledge_graph = knowledge_graph_core",
        "self.knowledge_graph = knowledge_graph_core\n        self.reasoning = reasoning_core",
        1,
    )

if 'self.commands.register("reason.evaluate"' not in text:
    anchor = 'self.commands.register("knowledge.statistics", self._cmd_kg_statistics)'
    if anchor not in text:
        raise SystemExit("knowledge.statistics anchor not found.")
    text = text.replace(
        anchor,
        anchor
        + """
        self.commands.register("reason.bootstrap", self._cmd_reason_bootstrap)
        self.commands.register("reason.rule.add", self._cmd_reason_rule_add)
        self.commands.register("reason.evaluate", self._cmd_reason_evaluate)
        self.commands.register("reason.explain", self._cmd_reason_explain)
        self.commands.register("reason.trace", self._cmd_reason_trace)
        self.commands.register("reason.decision", self._cmd_reason_decision)
        self.commands.register("reason.confidence", self._cmd_reason_confidence)
        self.commands.register("reason.statistics", self._cmd_reason_statistics)""",
    )

if '"Aletheus Cognitive Reasoning Engine"' not in text:
    service = """
        self.services.register(
            "Aletheus Cognitive Reasoning Engine",
            {"status": "online", "version": self.reasoning.version},
        )
"""
    marker = "        self.scheduler.register("
    if marker not in text:
        raise SystemExit("scheduler anchor not found.")
    text = text.replace(marker, service + "\n" + marker, 1)

if "def _cmd_reason_bootstrap" not in text:
    methods = """
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

"""
    anchor = "    def _job_runtime_pulse(self) -> dict:"
    if anchor not in text:
        raise SystemExit("_job_runtime_pulse anchor not found.")
    text = text.replace(anchor, methods + anchor, 1)

if '"reasoning_traces": self.reasoning.stats()["traces"]' not in text:
    text = text.replace(
        '"inference_rules": self.knowledge_graph.stats()["inference_rules"],',
        '"inference_rules": self.knowledge_graph.stats()["inference_rules"],\n                "reasoning_traces": self.reasoning.stats()["traces"],\n                "reasoning_rules": self.reasoning.stats()["rules"],\n                "reasoning_confidence": self.reasoning.stats()["confidence"],',
    )

p.write_text(text)
print("✔ v2.5 reasoning runtime patch applied.")
