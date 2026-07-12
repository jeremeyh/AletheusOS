from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from .drift import detect_drift
from .planner import create_build_plan
from .readiness import analyze_readiness


def generate_report(
    root: Path,
    output: Path,
) -> dict[str, object]:
    readiness = analyze_readiness(root)
    plan = create_build_plan(root)
    drift = detect_drift(root)

    payload = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "overall_readiness_percent":
            readiness[
                "overall_readiness_percent"
            ],
        "summary": {
            "implemented":
                readiness["implemented"],
            "partial":
                readiness["partial"],
            "blocked":
                readiness["blocked"],
            "missing":
                readiness["missing"],
            "drift_findings": len(drift),
        },
        "capabilities": [
            asdict(item)
            for item in readiness[
                "capabilities"
            ]
        ],
        "build_plan": [
            asdict(item)
            for item in plan
        ],
        "drift_findings": list(drift),
    }

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    return payload
