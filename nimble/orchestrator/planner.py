from __future__ import annotations

from pathlib import Path

from .discovery import discover_capabilities
from .models import BuildPlanItem


def create_build_plan(
    root: Path,
) -> tuple[BuildPlanItem, ...]:
    statuses = discover_capabilities(root)

    order_lookup = {
        status.capability_id: index
        for index, status in enumerate(
            statuses,
            start=1,
        )
    }

    plan: list[BuildPlanItem] = []

    for status in statuses:
        if status.state == "implemented":
            continue

        if status.state == "blocked":
            reason = "Blocked by: " + ", ".join(status.blocked_by)
            action = "resolve dependencies"
        elif status.state == "partial":
            reason = f"{len(status.missing_paths)} required path(s) missing"
            action = "complete capability"
        else:
            reason = "Capability not yet implemented"
            action = "build capability"

        plan.append(
            BuildPlanItem(
                order=order_lookup[status.capability_id],
                capability_id=status.capability_id,
                display_name=status.display_name,
                state=status.state,
                action=action,
                reason=reason,
            )
        )

    return tuple(
        sorted(
            plan,
            key=lambda item: (
                item.state == "blocked",
                item.order,
            ),
        )
    )
