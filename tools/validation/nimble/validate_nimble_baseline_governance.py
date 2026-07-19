from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

BASELINE = (
    ROOT
    / "nimble"
    / "governance"
    / "performance-baseline.json"
)

HISTORY_DIRECTORY = (
    ROOT
    / "nimble"
    / "governance"
    / "performance-baselines"
)

PROMOTION_REPORT = (
    ROOT
    / "reports"
    / "nimble"
    / "performance-baseline-promotion-latest.json"
)

REQUIRED_THRESHOLDS = {
    "primary_bundle_growth_percent",
    "primary_bundle_absolute_limit_bytes",
    "total_javascript_growth_percent",
    "largest_secondary_growth_percent",
    "secondary_chunk_count_decrease_allowed",
    "secondary_chunk_count_increase_allowed",
    "gate_duration_growth_percent",
    "gate_duration_absolute_limit_seconds",
}

REQUIRED_METRICS = {
    "primary_bundle_bytes",
    "secondary_chunk_count",
    "total_javascript_bytes",
    "largest_secondary_chunk_bytes",
    "gate_duration_seconds",
}


def load(
    path: Path,
) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def main() -> int:
    if not BASELINE.exists():
        print(
            "FAIL: Governed performance baseline is missing."
        )
        return 1

    baseline = load(BASELINE)

    missing_metrics = (
        REQUIRED_METRICS
        - set(baseline.get("metrics", {}))
    )

    if missing_metrics:
        print(
            "FAIL: Baseline metrics missing:",
            ", ".join(
                sorted(missing_metrics)
            ),
        )
        return 1

    missing_thresholds = (
        REQUIRED_THRESHOLDS
        - set(
            baseline.get(
                "thresholds",
                {},
            )
        )
    )

    if missing_thresholds:
        print(
            "FAIL: Baseline thresholds missing:",
            ", ".join(
                sorted(missing_thresholds)
            ),
        )
        return 1

    promotion = baseline.get("promotion")

    if promotion is None:
        print(
            "NOTICE: Baseline predates governed promotion."
        )
    else:
        rationale = str(
            promotion.get(
                "rationale",
                "",
            )
        ).strip()

        approved_by = str(
            promotion.get(
                "approved_by",
                "",
            )
        ).strip()

        archive = promotion.get(
            "archived_baseline"
        )

        if len(rationale) < 20:
            print(
                "FAIL: Baseline promotion rationale "
                "is missing or too short."
            )
            return 1

        if not approved_by:
            print(
                "FAIL: Baseline approval is missing."
            )
            return 1

        if not archive:
            print(
                "FAIL: Previous baseline archive "
                "was not recorded."
            )
            return 1

        archive_path = ROOT / archive

        if not archive_path.exists():
            print(
                "FAIL: Archived baseline is missing:",
                archive,
            )
            return 1

    history_files = sorted(
        HISTORY_DIRECTORY.glob(
            "performance-baseline-*.json"
        )
    )

    print("=" * 72)
    print("NIMBLE™ BASELINE GOVERNANCE VALIDATION")
    print("=" * 72)
    print("Current baseline: present")
    print(
        "Metrics:",
        len(REQUIRED_METRICS),
    )
    print(
        "Thresholds:",
        len(REQUIRED_THRESHOLDS),
    )
    print(
        "Archived baselines:",
        len(history_files),
    )
    print(
        "Governed promotion:",
        "active"
        if promotion is not None
        else "not yet performed",
    )
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
