from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# ------------------------------------------------------------
# Import
# ------------------------------------------------------------

if "from aletheus.planning_v2 import planning_core" not in text:
    text = text.replace(
        "from aletheus.workflow_v3 import workflow_core\n",
        "from aletheus.workflow_v3 import workflow_core\n"
        "from aletheus.planning_v2 import planning_core\n",
    )

# ------------------------------------------------------------
# Runtime initialization
# ------------------------------------------------------------

if "self.planning_v2 = planning_core" not in text:
    text = text.replace(
        "self.workflow_v3 = workflow_core",
        "self.workflow_v3 = workflow_core\n"
        "        self.planning_v2 = planning_core",
        1,
    )

# ------------------------------------------------------------
# Version
# ------------------------------------------------------------

text = text.replace('self.version = "2.8.0"', 'self.version = "2.9.0"')

# ------------------------------------------------------------
# Planning Service
# ------------------------------------------------------------

if "Aletheus Autonomous Planning Engine" not in text:
    marker = 'self.services.register("Aletheus Workflow Intelligence Engine"'

    start = text.find(marker)

    if start != -1:
        end = text.find("\n", start)

        insertion = '''
        self.services.register(
            "Aletheus Autonomous Planning Engine",
            {
                "status": "online",
                "version": self.planning_v2.VERSION,
            },
        )
'''

        text = text[:end + 1] + insertion + text[end + 1:]

# ------------------------------------------------------------
# Command Registration
# ------------------------------------------------------------

if 'self.commands.register("plan.bootstrap"' not in text:

    anchor = 'self.commands.register("workflow.statistics", self._cmd_workflow_statistics)'

    if anchor not in text:
        raise SystemExit("workflow.statistics registration not found.")

    text = text.replace(
        anchor,
        anchor + '''

        # v2.9 Planning Engine
        self.commands.register("plan.bootstrap", self._cmd_plan_bootstrap)
        self.commands.register("plan.create", self._cmd_plan_create)
        self.commands.register("plan.execute", self._cmd_plan_execute)
        self.commands.register("plan.progress", self._cmd_plan_progress)
        self.commands.register("plan.replan", self._cmd_plan_replan)
        self.commands.register("plan.complete", self._cmd_plan_complete)
        self.commands.register("plan.status", self._cmd_plan_status)
        self.commands.register("plan.statistics", self._cmd_plan_statistics)
''',
        1,
    )

core.write_text(text)

print("✔ v2.9 runtime integrated.")
