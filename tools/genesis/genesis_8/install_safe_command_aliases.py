from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ALIAS_MODULE = (
    ROOT
    / "aletheus/runtime/registrations/"
    / "compatibility_alias_commands.py"
)

BOOTSTRAPPER = (
    ROOT
    / "aletheus/runtime/command_bootstrap/bootstrapper.py"
)

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = (
    ROOT
    / "reports/genesis_8_command_dispatch"
    / f"safe_alias_backup_{stamp}"
)
backup.mkdir(parents=True, exist_ok=True)

shutil.copy2(
    BOOTSTRAPPER,
    backup / "bootstrapper.py",
)

if ALIAS_MODULE.exists():
    shutil.copy2(
        ALIAS_MODULE,
        backup / "compatibility_alias_commands.py",
    )


ALIAS_SOURCE = '''\
"""
Genesis 8 Safe Command Compatibility Aliases.

Only semantically equivalent namespace, version, or naming aliases belong
here. Fuzzy or cross-domain mappings are explicitly prohibited.
"""

from __future__ import annotations

from typing import Any


SAFE_COMMAND_ALIASES: dict[str, str] = {
    # Prediction namespace evolution.
    "predict.forecast": "prediction.forecast",
    "predict.scenario": "prediction.scenario",
    "predict.risks": "prediction.risks",
    "predict.opportunities": "prediction.opportunities",
    "predict.recommend": "prediction.recommend",

    # Learning namespace evolution.
    "learn.record": "learning.record",
    "learn.lesson": "learning.lesson",
    "learn.patterns": "learning.patterns",
    "learn.improve": "learning.improve",
    "learn.snapshot": "learning.snapshot",

    # Security naming normalization.
    "security.role.create": "security.role_create",
    "security.role.assign": "security.role_assign",

    # Statistics naming normalization.
    "cluster.stats": "cluster.statistics",
    "mission.stats": "mission.statistics",

    # Mission v2 public compatibility names.
    "mission.v2.create": "mission.create",
    "mission.v2.execute": "mission.execute",
    "mission.v2.stats": "mission.statistics",

    # Workflow v2 public compatibility names.
    "workflow.v2.create": "workflow.create",
    "workflow.v2.stats": "workflow.statistics",

    # Kernel public compatibility names.
    "kernel.boot": "kernel.bootstrap",
    "kernel.publish": "event.publish",
}


def register_compatibility_alias_commands(runtime: Any) -> None:
    registry = runtime.commands.registry
    dispatcher = registry.dispatcher

    for alias, canonical in SAFE_COMMAND_ALIASES.items():
        if registry.has(alias):
            continue

        record = registry.get(canonical)

        if record is None:
            raise RuntimeError(
                f"Cannot register alias {alias!r}: "
                f"canonical command {canonical!r} is missing."
            )

        metadata = dict(record.metadata)
        metadata["alias_for"] = canonical
        metadata["compatibility_alias"] = True

        canonical_result_key = (
            dispatcher.RESULT_KEY_CONTRACTS.get(canonical)
        )

        if canonical_result_key is not None:
            metadata.setdefault(
                "result_key",
                canonical_result_key,
            )

        registry.register(
            alias,
            record.handler,
            category=record.category,
            metadata=metadata,
            replace=False,
        )
'''

ALIAS_MODULE.write_text(
    ALIAS_SOURCE,
    encoding="utf-8",
)


bootstrap_text = BOOTSTRAPPER.read_text(
    encoding="utf-8"
)

import_line = (
    "from aletheus.runtime.registrations."
    "compatibility_alias_commands import "
    "register_compatibility_alias_commands"
)

if import_line not in bootstrap_text:
    class_marker = "\n\nclass RuntimeCommandBootstrapper:"

    if class_marker not in bootstrap_text:
        raise RuntimeError(
            "RuntimeCommandBootstrapper class marker not found."
        )

    bootstrap_text = bootstrap_text.replace(
        class_marker,
        f"\n{import_line}{class_marker}",
        1,
    )


call_line = (
    "        register_compatibility_alias_commands(runtime)"
)

if call_line not in bootstrap_text:
    anchor = "        register_governance_commands(runtime)"

    if anchor not in bootstrap_text:
        raise RuntimeError(
            "Governance registration anchor not found."
        )

    bootstrap_text = bootstrap_text.replace(
        anchor,
        (
            anchor
            + "\n\n"
            + "        # Explicit compile-time compatibility aliases.\n"
            + call_line
        ),
        1,
    )


BOOTSTRAPPER.write_text(
    bootstrap_text,
    encoding="utf-8",
)

print("Genesis 8 safe command aliases installed.")
print(f"Backup: {backup.relative_to(ROOT)}")
print(f"Created: {ALIAS_MODULE.relative_to(ROOT)}")
print(f"Updated: {BOOTSTRAPPER.relative_to(ROOT)}")
print(f"Alias count: {len(SAFE_COMMAND_ALIASES)}")
