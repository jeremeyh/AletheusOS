from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
LATEST_REPORT = (
    ROOT
    / "reports"
    / "nimble"
    / "production-gate-latest.json"
)
BASELINE_PATH = (
    ROOT
    / "nimble"
    / "governance"
    / "performance-baseline.json"
)


def main() -> int:
    if not LATEST_REPORT.exists():
        print(
            "FAIL: Production telemetry is missing. "
            "Run collect_nimble_production_telemetry.py first."
        )
        return 1

    report: dict[str, Any] = json.loads(
        LATEST_REPORT.read_text(encoding="utf-8")
    )

    gate = report["gate"]
    bundle = report["bundle"]
    git = report["git"]

    primary = bundle.get("primary")

    if primary is None:
        print("FAIL: Current telemetry has no primary bundle.")
        return 1

    secondary_chunks = [
        chunk
        for chunk in bundle["chunks"]
        if chunk["kind"] == "secondary"
    ]

    baseline = {
        "schema_version": "1.0",
        "created_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "source": {
            "commit": git["commit"],
            "short_commit": git["short_commit"],
            "branch": git["branch"],
            "telemetry_generated_at": report[
                "generated_at"
            ],
        },
        "metrics": {
            "primary_bundle_bytes": primary["bytes"],
            "secondary_chunk_count": bundle[
                "secondary_chunk_count"
            ],
            "total_javascript_bytes": sum(
                chunk["bytes"]
                for chunk in bundle["chunks"]
            ),
            "largest_secondary_chunk_bytes": max(
                (
                    chunk["bytes"]
                    for chunk in secondary_chunks
                ),
                default=0,
            ),
            "gate_duration_seconds": gate[
                "duration_seconds"
            ],
        },
        "thresholds": {
            "primary_bundle_growth_percent": 5.0,
            "primary_bundle_absolute_limit_bytes": 500000,
            "total_javascript_growth_percent": 10.0,
            "largest_secondary_growth_percent": 15.0,
            "secondary_chunk_count_decrease_allowed": 1,
            "secondary_chunk_count_increase_allowed": 4,
            "gate_duration_growth_percent": 35.0,
            "gate_duration_absolute_limit_seconds": 120.0
        },
    }

    BASELINE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    BASELINE_PATH.write_text(
        json.dumps(
            baseline,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ PERFORMANCE BASELINE")
    print("=" * 72)
    print(
        "Primary bundle:",
        f"{baseline['metrics']['primary_bundle_bytes']:,} bytes",
    )
    print(
        "Secondary chunks:",
        baseline["metrics"]["secondary_chunk_count"],
    )
    print(
        "Total JavaScript:",
        f"{baseline['metrics']['total_javascript_bytes']:,} bytes",
    )
    print(
        "Gate duration:",
        f"{baseline['metrics']['gate_duration_seconds']:.2f}s",
    )
    print(
        "Baseline:",
        BASELINE_PATH.relative_to(ROOT),
    )
    print("Status: CREATED")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
