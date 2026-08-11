from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# ------------------------------------------------------------------
# Import
# ------------------------------------------------------------------

if "from aletheus.agents_v2 import agent_core" not in text:
    text = text.replace(
        "from aletheus.decision_v2 import decision_core\n",
        "from aletheus.decision_v2 import decision_core\n"
        "from aletheus.agents_v2 import agent_core\n",
    )

# ------------------------------------------------------------------
# Runtime initialization
# ------------------------------------------------------------------

if "self.agents_v2 = agent_core" not in text:
    text = text.replace(
        "self.decision = decision_core",
        "self.decision = decision_core\n        self.agents_v2 = agent_core",
        1,
    )

# ------------------------------------------------------------------
# Version
# ------------------------------------------------------------------

text = text.replace('self.version = "2.6.0"', 'self.version = "2.7.0"')

# ------------------------------------------------------------------
# Service registration
# ------------------------------------------------------------------

if "Aletheus Autonomous Agent Runtime" not in text:
    marker = 'self.services.register("Aletheus Autonomous Decision Engine"'
    start = text.find(marker)

    if start != -1:
        end = text.find("\n", start)
        insertion = """
        self.services.register(
            "Aletheus Autonomous Agent Runtime",
            {
                "status": "online",
                "version": self.agents_v2.VERSION,
            },
        )
"""
        text = text[: end + 1] + insertion + text[end + 1 :]

# ------------------------------------------------------------------
# Command registration
# ------------------------------------------------------------------

if 'self.commands.register("agent.bootstrap"' not in text:
    anchor = (
        'self.commands.register("decision.statistics", self._cmd_decision_statistics)'
    )

    text = text.replace(
        anchor,
        anchor
        + """

        # v2.7 Autonomous Agent Runtime
        self.commands.register("agent.bootstrap", self._cmd_agent_bootstrap)
        self.commands.register("agent.spawn", self._cmd_agent_spawn)
        self.commands.register("agent.assign", self._cmd_agent_assign)
        self.commands.register("agent.message", self._cmd_agent_message)
        self.commands.register("agent.pause", self._cmd_agent_pause)
        self.commands.register("agent.resume", self._cmd_agent_resume)
        self.commands.register("agent.stop", self._cmd_agent_stop)
        self.commands.register("agent.heartbeat", self._cmd_agent_heartbeat)
        self.commands.register("agent.statistics", self._cmd_agent_statistics)
""",
        1,
    )

core.write_text(text)

print("✔ v2.7 runtime patched.")
