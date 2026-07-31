from pathlib import Path

CORE = Path("aletheus/runtime/core.py")
REG_INIT = Path("aletheus/runtime/registrations/__init__.py")

required_modules = [
    "runtime_commands.py",
    "memory_commands.py",
    "reasoning_commands.py",
    "decision_commands.py",
    "graph_commands.py",
    "mission_commands.py",
    "workspace_commands.py",
    "application_commands.py",
    "semantic_commands.py",
    "executive_commands.py",
    "agent_commands.py",
    "planning_commands.py",
    "copilot_commands.py",
    "uil_commands.py",
]

missing = [
    name
    for name in required_modules
    if not Path("aletheus/runtime/registrations", name).exists()
]

if missing:
    raise SystemExit(f"Missing registration modules: {missing}")

REG_INIT.write_text('''"""
AletheusOS Runtime Registration Package

Version 5.0.1
"""

from .runtime_commands import register_runtime_commands
from .memory_commands import register_memory_commands
from .reasoning_commands import register_reasoning_commands
from .decision_commands import register_decision_commands
from .graph_commands import register_graph_commands
from .mission_commands import register_mission_commands
from .workspace_commands import register_workspace_commands
from .application_commands import register_application_commands
from .semantic_commands import register_semantic_commands
from .executive_commands import register_executive_commands
from .agent_commands import register_agent_commands
from .planning_commands import register_planning_commands
from .copilot_commands import register_copilot_commands
from .uil_commands import register_uil_commands

__all__ = [
    "register_runtime_commands",
    "register_memory_commands",
    "register_reasoning_commands",
    "register_decision_commands",
    "register_graph_commands",
    "register_mission_commands",
    "register_workspace_commands",
    "register_application_commands",
    "register_semantic_commands",
    "register_executive_commands",
    "register_agent_commands",
    "register_planning_commands",
    "register_copilot_commands",
    "register_uil_commands",
]
''')

text = CORE.read_text()
lines = text.splitlines(keepends=True)

# Remove any existing registrations import, single-line or multi-line.
cleaned = []
i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith("from aletheus.runtime.registrations import"):
        if "(" in line and ")" not in line:
            i += 1
            while i < len(lines) and ")" not in lines[i]:
                i += 1
            if i < len(lines):
                i += 1
            continue
        i += 1
        continue

    cleaned.append(line)
    i += 1

canonical_import = """from aletheus.runtime.registrations import (
    register_runtime_commands,
    register_memory_commands,
    register_reasoning_commands,
    register_decision_commands,
    register_graph_commands,
    register_mission_commands,
    register_workspace_commands,
    register_application_commands,
    register_semantic_commands,
    register_executive_commands,
    register_agent_commands,
    register_planning_commands,
    register_copilot_commands,
    register_uil_commands,
)
"""

text = "".join(cleaned)

anchor = "from aletheus.runtime.services import ServiceRegistry\n"

if anchor not in text:
    raise SystemExit("Could not find ServiceRegistry import anchor in core.py")

text = text.replace(anchor, anchor + canonical_import, 1)

CORE.write_text(text)

print("✔ core.py registration imports normalized.")
print("✔ registrations/__init__.py fully rebuilt.")
