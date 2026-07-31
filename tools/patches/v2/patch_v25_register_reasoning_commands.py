from pathlib import Path

core = Path("aletheus/runtime/core.py")

text = core.read_text()

if 'self.commands.register("reason.bootstrap"' in text:
    print("Reasoning commands already registered.")
    raise SystemExit(0)

anchor = 'self.commands.register("knowledge.statistics", self._cmd_kg_statistics)'

if anchor not in text:
    raise SystemExit("Could not locate knowledge.statistics registration.")

replacement = (
    anchor
    + """

        # v2.5 Cognitive Reasoning Engine
        self.commands.register("reason.bootstrap", self._cmd_reason_bootstrap)
        self.commands.register("reason.rule.add", self._cmd_reason_rule_add)
        self.commands.register("reason.evaluate", self._cmd_reason_evaluate)
        self.commands.register("reason.explain", self._cmd_reason_explain)
        self.commands.register("reason.trace", self._cmd_reason_trace)
        self.commands.register("reason.decision", self._cmd_reason_decision)
        self.commands.register("reason.confidence", self._cmd_reason_confidence)
        self.commands.register("reason.statistics", self._cmd_reason_statistics)
"""
)

text = text.replace(anchor, replacement, 1)

core.write_text(text)

print("✔ Reasoning commands registered.")
