from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# ----------------------------------------------------
# Import Workflow Engine
# ----------------------------------------------------

if "from aletheus.workflow_v3 import workflow_core" not in text:
    text = text.replace(
        "from aletheus.agents_v2 import agent_core\n",
        "from aletheus.agents_v2 import agent_core\n"
        "from aletheus.workflow_v3 import workflow_core\n",
    )

# ----------------------------------------------------
# Runtime initialization
# ----------------------------------------------------

if "self.workflow_v3 = workflow_core" not in text:
    text = text.replace(
        "self.agents_v2 = agent_core",
        "self.agents_v2 = agent_core\n"
        "        self.workflow_v3 = workflow_core",
        1,
    )

# ----------------------------------------------------
# Runtime version
# ----------------------------------------------------

text = text.replace('self.version = "2.7.0"', 'self.version = "2.8.0"')

# ----------------------------------------------------
# Register Workflow service
# ----------------------------------------------------

if "Aletheus Workflow Intelligence Engine" not in text:
    marker = 'self.services.register("Aletheus Autonomous Agent Runtime"'

    start = text.find(marker)

    if start != -1:
        end = text.find("\n", start)

        insertion = '''
        self.services.register(
            "Aletheus Workflow Intelligence Engine",
            {
                "status": "online",
                "version": self.workflow_v3.VERSION,
            },
        )
'''

        text = text[:end + 1] + insertion + text[end + 1:]

# ----------------------------------------------------
# Register commands
# ----------------------------------------------------

if 'self.commands.register("workflow.bootstrap"' not in text:

    anchor = 'self.commands.register("agent.statistics", self._cmd_agent_statistics)'

    if anchor not in text:
        raise SystemExit("agent.statistics registration not found.")

    text = text.replace(
        anchor,
        anchor + '''

        # v2.8 Workflow Intelligence
        self.commands.register("workflow.bootstrap", self._cmd_workflow_bootstrap)
        self.commands.register("workflow.create", self._cmd_workflow_create)
        self.commands.register("workflow.start", self._cmd_workflow_start)
        self.commands.register("workflow.pause", self._cmd_workflow_pause)
        self.commands.register("workflow.resume", self._cmd_workflow_resume)
        self.commands.register("workflow.cancel", self._cmd_workflow_cancel)
        self.commands.register("workflow.status", self._cmd_workflow_status)
        self.commands.register("workflow.statistics", self._cmd_workflow_statistics)
''',
        1,
    )

core.write_text(text)

print("✔ v2.8 runtime integration complete.")
