from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BOOTSTRAPPER = (
    ROOT
    / "aletheus/runtime/command_bootstrap/bootstrapper.py"
)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = (
    ROOT
    / "reports/genesis_8_command_dispatch"
    / f"registration_catalog_backup_{stamp}"
)
backup_dir.mkdir(parents=True, exist_ok=True)

shutil.copy2(
    BOOTSTRAPPER,
    backup_dir / "bootstrapper.py",
)

text = BOOTSTRAPPER.read_text(encoding="utf-8")


IMPORTS = [
    (
        "aletheus.runtime.registrations.agent_commands",
        "register_agent_commands",
    ),
    (
        "aletheus.runtime.registrations.application_commands",
        "register_application_commands",
    ),
    (
        "aletheus.runtime.registrations.compatibility_commands",
        "register_compatibility_commands",
    ),
    (
        "aletheus.runtime.registrations.copilot_commands",
        "register_copilot_commands",
    ),
    (
        "aletheus.runtime.registrations.decision_commands",
        "register_decision_commands",
    ),
    (
        "aletheus.runtime.registrations.executive_commands",
        "register_executive_commands",
    ),
    (
        "aletheus.runtime.registrations.graph_commands",
        "register_graph_commands",
    ),
    (
        "aletheus.runtime.registrations.mission_commands",
        "register_mission_commands",
    ),
    (
        "aletheus.runtime.registrations.planning_commands",
        "register_planning_commands",
    ),
    (
        "aletheus.runtime.registrations.semantic_commands",
        "register_semantic_commands",
    ),
    (
        "aletheus.runtime.registrations.uil_commands",
        "register_uil_commands",
    ),
    (
        "aletheus.runtime.registrations.workspace_commands",
        "register_workspace_commands",
    ),
]


def import_statement(module: str, function: str) -> str:
    return f"from {module} import {function}"


missing_imports = [
    import_statement(module, function)
    for module, function in IMPORTS
    if import_statement(module, function) not in text
]

if missing_imports:
    lines = text.splitlines()

    last_import_index = -1

    for index, line in enumerate(lines):
        if line.startswith("from ") or line.startswith("import "):
            last_import_index = index
        elif last_import_index >= 0 and line.strip():
            break

    if last_import_index < 0:
        raise RuntimeError(
            "Could not locate bootstrapper import section."
        )

    lines[
        last_import_index + 1:last_import_index + 1
    ] = missing_imports

    text = "\n".join(lines) + "\n"


CALLS = [
    "register_graph_commands(runtime)",
    "register_mission_commands(runtime)",
    "register_workspace_commands(runtime)",
    "register_application_commands(runtime)",
    "register_semantic_commands(runtime)",
    "register_executive_commands(runtime)",
    "register_agent_commands(runtime)",
    "register_planning_commands(runtime)",
    "register_copilot_commands(runtime)",
    "register_uil_commands(runtime)",
    "register_decision_commands(runtime)",
    "register_compatibility_commands(runtime)",
]

missing_calls = [
    call
    for call in CALLS
    if call not in text
]

if missing_calls:
    anchor = "        register_governance_commands(runtime)"

    if anchor not in text:
        raise RuntimeError(
            "Could not locate final governance registration "
            "call in RuntimeCommandBootstrapper."
        )

    compatibility_phase = "\n".join(
        [
            "",
            "        # Legacy and compatibility command families.",
            "        # These remain first-class bootstrap registrations",
            "        # until their public contracts are formally retired.",
            *[
                f"        {call}"
                for call in missing_calls
            ],
        ]
    )

    text = text.replace(
        anchor,
        anchor + compatibility_phase,
        1,
    )


BOOTSTRAPPER.write_text(
    text,
    encoding="utf-8",
)

print("Genesis 8 registration catalog restored.")
print(f"Backup: {backup_dir.relative_to(ROOT)}")
print(f"Updated: {BOOTSTRAPPER.relative_to(ROOT)}")
print(f"Imports added: {len(missing_imports)}")
print(f"Calls added: {len(missing_calls)}")
