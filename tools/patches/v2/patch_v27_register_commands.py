from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

if 'self.commands.register("agent.spawn"' in text:
    print("Agent commands already registered.")
    raise SystemExit(0)

anchor = 'self.commands.register("decision.statistics", self._cmd_decision_statistics)'

if anchor not in text:
    raise SystemExit("Could not find decision.statistics registration.")

replacement = anchor + '''

        # -----------------------------
        # v2.7 Autonomous Agent Runtime
        # -----------------------------
        self.commands.register("agent.bootstrap", self._cmd_agent_bootstrap)
        self.commands.register("agent.spawn", self._cmd_agent_spawn)
        self.commands.register("agent.assign", self._cmd_agent_assign)
        self.commands.register("agent.message", self._cmd_agent_message)
        self.commands.register("agent.pause", self._cmd_agent_pause)
        self.commands.register("agent.resume", self._cmd_agent_resume)
        self.commands.register("agent.stop", self._cmd_agent_stop)
        self.commands.register("agent.heartbeat", self._cmd_agent_heartbeat)
        self.commands.register("agent.statistics", self._cmd_agent_statistics)
'''

text = text.replace(anchor, replacement, 1)

path.write_text(text)

print("✔ Agent commands registered.")
