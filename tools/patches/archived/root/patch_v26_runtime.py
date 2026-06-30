from pathlib import Path

p = Path("aletheus/runtime/core.py")
text = p.read_text()

if "from aletheus.decision_v2 import decision_core" not in text:
    text = text.replace(
        "from aletheus.reasoning import reasoning_core\n",
        "from aletheus.reasoning import reasoning_core\nfrom aletheus.decision_v2 import decision_core\n",
    )

text = text.replace('self.version = "2.5.0"', 'self.version = "2.6.0"')

if "self.decision = decision_core" not in text:
    text = text.replace(
        "self.reasoning = reasoning_core",
        "self.reasoning = reasoning_core\n        self.decision = decision_core",
        1,
    )

if 'self.commands.register("decision.bootstrap"' not in text:
    anchor = 'self.commands.register("reason.statistics", self._cmd_reason_statistics)'
    if anchor not in text:
        raise SystemExit("reason.statistics anchor not found.")
    text = text.replace(
        anchor,
        anchor + '''

        # v2.6 Autonomous Decision Engine
        self.commands.register("decision.bootstrap", self._cmd_decision_bootstrap)
        self.commands.register("decision.policy.add", self._cmd_decision_policy_add)
        self.commands.register("decision.evaluate", self._cmd_decision_evaluate)
        self.commands.register("decision.execute", self._cmd_decision_execute)
        self.commands.register("decision.rollback", self._cmd_decision_rollback)
        self.commands.register("decision.explain", self._cmd_decision_explain)
        self.commands.register("decision.history", self._cmd_decision_history)
        self.commands.register("decision.statistics", self._cmd_decision_statistics)''',
        1,
    )

if "Aletheus Autonomous Decision Engine" not in text:
    service = '''
        self.services.register(
            "Aletheus Autonomous Decision Engine",
            {"status": "online", "version": self.decision.version},
        )
'''
    marker = "        self.scheduler.register("
    if marker not in text:
        raise SystemExit("scheduler anchor not found.")
    text = text.replace(marker, service + "\n" + marker, 1)

if "def _cmd_decision_bootstrap" not in text:
    methods = '''
    def _cmd_decision_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("decision", self.decision.bootstrap())
        return context

    def _cmd_decision_policy_add(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.decision.add_policy(
            name=payload.get("name", "Untitled Policy"),
            description=payload.get("description", ""),
            policy_type=payload.get("policy_type", "general"),
            weight=float(payload.get("weight", 1.0)),
        )
        context.add_result("policy", result)
        return context

    def _cmd_decision_evaluate(self, context: RuntimeContext) -> RuntimeContext:
        payload = context.payload
        result = self.decision.evaluate(
            title=payload.get("title", "Untitled Decision"),
            objective=payload.get("objective", ""),
            options=payload.get("options", []),
            policy=payload.get("policy", "maximize_value"),
            runtime=self,
        )
        context.add_result("decision", result)
        return context

    def _cmd_decision_execute(self, context: RuntimeContext) -> RuntimeContext:
        result = self.decision.execute(context.payload.get("decision_id", ""))
        context.add_result("decision", result)
        return context

    def _cmd_decision_rollback(self, context: RuntimeContext) -> RuntimeContext:
        result = self.decision.rollback(context.payload.get("decision_id", ""))
        context.add_result("decision", result)
        return context

    def _cmd_decision_explain(self, context: RuntimeContext) -> RuntimeContext:
        result = self.decision.explain(context.payload.get("decision_id", ""))
        context.add_result("explanation", result)
        return context

    def _cmd_decision_history(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("history", self.decision.history())
        return context

    def _cmd_decision_statistics(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result("decision_stats", self.decision.stats())
        return context

'''
    anchor = "    def _job_runtime_pulse(self) -> dict:"
    if anchor not in text:
        raise SystemExit("_job_runtime_pulse anchor not found.")
    text = text.replace(anchor, methods + anchor, 1)

if '"decision_stats": self.decision.stats()' not in text:
    text = text.replace(
        '''        context.add_result("reasoning", self.reasoning.stats())
        return context
''',
        '''        context.add_result("reasoning", self.reasoning.stats())
        context.add_result("decision", self.decision.stats())
        return context
''',
    )

p.write_text(text)
print("✔ v2.6 decision runtime patch applied.")
