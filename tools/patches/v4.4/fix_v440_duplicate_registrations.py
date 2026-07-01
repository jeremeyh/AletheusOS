from pathlib import Path

CORE = Path("aletheus/runtime/core.py")

text = CORE.read_text()

targets = [
    'self.commands.register("reason.evaluate", self._cmd_reason_evaluate)',
    'self.commands.register("decision.history", self._cmd_decision_history)',
    'self.commands.register("agent.bootstrap", self._cmd_agent_bootstrap)',
]

changed = False

for target in targets:
    first = text.find(target)
    if first == -1:
        continue

    second = text.find(target, first + len(target))
    if second == -1:
        continue

    line_end = text.find("\n", second)
    if line_end == -1:
        line_end = len(text)

    text = text[:second] + text[line_end + 1 :]
    changed = True
    print(f"Removed duplicate: {target}")

if changed:
    CORE.write_text(text)
    print("\n✔ Duplicate command registrations removed.")
else:
    print("\n✔ No duplicate registrations found.")
