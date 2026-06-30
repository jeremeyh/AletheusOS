from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# 1. Register reasoning commands if missing
if 'self.commands.register("reason.bootstrap"' not in text:
    anchor = 'self.commands.register("knowledge.statistics", self._cmd_kg_statistics)'
    if anchor not in text:
        raise SystemExit("Could not locate knowledge.statistics registration anchor.")

    text = text.replace(
        anchor,
        anchor + '''

        # v2.5 Cognitive Reasoning Engine
        self.commands.register("reason.bootstrap", self._cmd_reason_bootstrap)
        self.commands.register("reason.rule.add", self._cmd_reason_rule_add)
        self.commands.register("reason.evaluate", self._cmd_reason_evaluate)
        self.commands.register("reason.explain", self._cmd_reason_explain)
        self.commands.register("reason.trace", self._cmd_reason_trace)
        self.commands.register("reason.decision", self._cmd_reason_decision)
        self.commands.register("reason.confidence", self._cmd_reason_confidence)
        self.commands.register("reason.statistics", self._cmd_reason_statistics)
''',
        1,
    )

# 2. Add command handlers if missing
if "def _cmd_reason_bootstrap" not in text:
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
        result = self.reasoning.explain(
            trace_id=context.payload.get("trace_id", ""),
        )
        context.add_result("explanation", result)
        return context

    def _cmd_reason_trace(self, context: RuntimeContext) -> RuntimeContext:
        result = self.reasoning.trace(
            trace_id=context.payload.get("trace_id", ""),
        )
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
    anchor = "    def _job_runtime_pulse(self) -> dict:"
    if anchor not in text:
        raise SystemExit("Could not locate _job_runtime_pulse anchor.")
    text = text.replace(anchor, methods + anchor, 1)

core.write_text(text)
print("✔ v2.5 reasoning commands and handlers patched.")
