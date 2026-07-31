"""Build bounded execution units."""

from __future__ import annotations

from typing import Any

from .models import ExecutionUnit

_RISK_ORDER = {"low": 0, "medium": 1, "high": 2}


def build_units(
    roadmap: dict[str, Any],
) -> tuple[list[ExecutionUnit], list[str]]:
    raw_packages = roadmap.get("work_packages", [])
    if not isinstance(raw_packages, list):
        raise TypeError("work_packages must be a list.")

    units: list[ExecutionUnit] = []
    abstentions: list[str] = []

    for index, item in enumerate(raw_packages):
        if not isinstance(item, dict):
            abstentions.append(f"Skipped malformed work package at index {index}.")
            continue

        package_id = str(item.get("package_id", f"package-{index}"))
        title = str(item.get("title", package_id))
        category = str(item.get("category", "unknown"))
        phase = int(item.get("phase", 99))
        risk = str(item.get("risk", "high"))
        effort = str(item.get("estimated_effort", "high"))
        gain = float(item.get("expected_health_gain", 0.0))

        candidate_ids_raw = item.get("candidate_ids")
        if candidate_ids_raw is None:
            candidates = item.get("candidates", [])
            candidate_ids_raw = (
                [
                    value.get("candidate_id")
                    for value in candidates
                    if isinstance(value, dict)
                ]
                if isinstance(candidates, list)
                else []
            )

        if not isinstance(candidate_ids_raw, list | tuple):
            abstentions.append(f"Skipped {package_id}: candidate_ids are invalid.")
            continue

        candidate_ids = tuple(
            str(value) for value in candidate_ids_raw if value is not None
        )
        if not candidate_ids:
            abstentions.append(
                f"Skipped {package_id}: no candidate evidence is attached."
            )
            continue

        preconditions = [
            "Repository working tree has no overlapping protected changes.",
            "Optimization roadmap source exists and is parseable.",
            "A Git checkpoint can be created.",
        ]
        validations = [
            "Run Ruff on changed targets.",
            "Compile changed Python packages.",
            "Run targeted tests.",
            "Regenerate Kinekt integrity and constitutional health reports.",
        ]
        rollback = [
            "Preserve file backups before mutation.",
            "Preserve a rollback manifest.",
            "Restore automatically when validation fails.",
        ]

        if risk == "high":
            preconditions.append(
                "High-risk execution unit must be approved independently."
            )
            validations.append("Run full platform test suite before completion.")

        units.append(
            ExecutionUnit(
                unit_id=f"eu-{package_id}",
                title=title,
                phase=phase,
                category=category,
                candidate_ids=candidate_ids,
                risk=risk,
                effort=effort,
                expected_health_gain=round(gain, 2),
                preconditions=tuple(preconditions),
                validations=tuple(validations),
                rollback_requirements=tuple(rollback),
            )
        )

    units.sort(
        key=lambda unit: (
            unit.phase,
            _RISK_ORDER.get(unit.risk, 3),
            -unit.expected_health_gain,
            unit.unit_id,
        )
    )
    return units, abstentions
