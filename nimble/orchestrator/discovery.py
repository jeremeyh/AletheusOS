from __future__ import annotations

from pathlib import Path

from .manifest import CAPABILITIES
from .models import CapabilityStatus


def discover_capabilities(
    root: Path,
) -> tuple[CapabilityStatus, ...]:
    provisional: dict[str, CapabilityStatus] = {}

    for definition in CAPABILITIES:
        existing = tuple(
            path for path in definition.required_paths if (root / path).exists()
        )

        missing = tuple(
            path for path in definition.required_paths if not (root / path).exists()
        )

        required_count = len(definition.required_paths)

        readiness = (
            round(len(existing) / required_count * 100) if required_count else 100
        )

        if readiness == 100:
            state = "implemented"
        elif readiness == 0:
            state = "missing"
        else:
            state = "partial"

        provisional[definition.capability_id] = CapabilityStatus(
            capability_id=definition.capability_id,
            display_name=definition.display_name,
            state=state,
            readiness_percent=readiness,
            existing_paths=existing,
            missing_paths=missing,
            dependencies=definition.dependencies,
            blocked_by=(),
            constitutional=definition.constitutional,
        )

    resolved: list[CapabilityStatus] = []

    for definition in CAPABILITIES:
        status = provisional[definition.capability_id]

        blocked_by = tuple(
            dependency
            for dependency in definition.dependencies
            if provisional[dependency].state != "implemented"
        )

        state = status.state

        if state != "implemented" and blocked_by:
            state = "blocked"

        resolved.append(
            CapabilityStatus(
                capability_id=status.capability_id,
                display_name=status.display_name,
                state=state,
                readiness_percent=status.readiness_percent,
                existing_paths=status.existing_paths,
                missing_paths=status.missing_paths,
                dependencies=status.dependencies,
                blocked_by=blocked_by,
                constitutional=status.constitutional,
            )
        )

    return tuple(resolved)
