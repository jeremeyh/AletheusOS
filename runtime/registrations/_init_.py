"""
AletheusOS Runtime Registration Package

Version 4.8.1
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
