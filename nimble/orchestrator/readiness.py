from __future__ import annotations

from pathlib import Path

from .discovery import discover_capabilities
from .models import CapabilityStatus


def analyze_readiness(
    root: Path,
) -> dict[str, object]:
    capabilities = discover_capabilities(
        root
    )

    implemented = sum(
        item.state == "implemented"
        for item in capabilities
    )

    partial = sum(
        item.state == "partial"
        for item in capabilities
    )

    blocked = sum(
        item.state == "blocked"
        for item in capabilities
    )

    missing = sum(
        item.state == "missing"
        for item in capabilities
    )

    overall = round(
        sum(
            item.readiness_percent
            for item in capabilities
        )
        / len(capabilities)
    )

    return {
        "overall_readiness_percent": overall,
        "implemented": implemented,
        "partial": partial,
        "blocked": blocked,
        "missing": missing,
        "capabilities": capabilities,
    }
