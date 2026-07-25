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

    # Workflow v2 public compatibility names.

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
