#!/bin/bash

set -e

echo "=== Genesis 7 Core Composition Cleanup ==="


cp aletheus/runtime/core.py \
   aletheus/runtime/core.py.genesis7_backup


echo "Backup created."


python - <<'PY'
from pathlib import Path

path = Path("aletheus/runtime/core.py")

text = path.read_text()


# Remove extracted command imports
remove_blocks = [
"""
from aletheus.runtime.registrations import (
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
]


for block in remove_blocks:
    text = text.replace(block, "")


# Add composition imports

marker = "from aletheus.runtime.integrity import RuntimeInvariantEngine, RuntimeBootValidator"


addition = """

from aletheus.runtime.adapters.graph_adapter import GraphCommandAdapter
from aletheus.runtime.adapters.mission_adapter import MissionCommandAdapter
from aletheus.runtime.adapters.event_adapter import EventCommandAdapter
from aletheus.runtime.adapters.runtime_adapter import RuntimeCommandAdapter
from aletheus.runtime.adapters.compatibility_adapter import CompatibilityCommandAdapter

"""


if "CompatibilityCommandAdapter" not in text:

    text = text.replace(
        marker,
        marker + addition
    )


path.write_text(text)

PY



echo "Removing duplicated compatibility handlers..."


python - <<'PY'
from pathlib import Path
import re

path = Path("aletheus/runtime/core.py")

text = path.read_text()


patterns = [
    r"\n    def _cmd_compat_list\(.*?(?=\n    def )",
    r"\n    def _cmd_compat_statistics\(.*?(?=\n    def )",
    r"\n    def _cmd_compat_resolve\(.*?(?=\n    def )",
    r"\n    def _cmd_compat_contract\(.*?(?=\n    def )",
]


for pattern in patterns:

    text = re.sub(
        pattern,
        "\n",
        text,
        flags=re.S
    )


path.write_text(text)

PY



echo "Removing graph adapter handlers..."


python - <<'PY'
from pathlib import Path
import re


path = Path("aletheus/runtime/core.py")

text = path.read_text()


functions = [
"_cmd_entity_create",
"_cmd_entity_search",
"_cmd_relationship_create",
"_cmd_relationship_search",
"_cmd_graph_export",
"_cmd_graph_query",
"_cmd_graph_stats",
]


for fn in functions:

    pattern = (
        r"\n    def "
        + fn
        + r"\(.*?(?=\n    def )"
    )

    text = re.sub(
        pattern,
        "\n",
        text,
        flags=re.S
    )


path.write_text(text)

PY



echo "Removing mission handlers..."


python - <<'PY'
from pathlib import Path
import re


path = Path("aletheus/runtime/core.py")

text = path.read_text()


functions = [
"_cmd_mission_create",
"_cmd_mission_from_goal",
"_cmd_mission_list",
"_cmd_mission_run",
"_cmd_mission_complete",
"_cmd_mission_task_complete",
"_cmd_mission_history",
"_cmd_mission_stats",
]


for fn in functions:

    pattern = (
        r"\n    def "
        + fn
        + r"\(.*?(?=\n    def )"
    )

    text = re.sub(
        pattern,
        "\n",
        text,
        flags=re.S
    )


path.write_text(text)

PY



echo "Compile..."

python -m compileall aletheus/runtime



echo "Runtime validation..."

python - <<'PY'
from aletheus.runtime import runtime_core


print(
{
"commands":
runtime_core.commands.count(),

"genesis6":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"],

"core_lines":
len(open("aletheus/runtime/core.py").readlines())
}
)

PY



echo "=== Genesis 7 Core Cleanup Complete ==="

