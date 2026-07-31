from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)


CURRENT_BASELINE = ROOT / "nimble" / "governance" / "performance-baseline.json"

BASELINE_HISTORY = ROOT / "nimble" / "governance" / "performance-baselines"

LATEST_TELEMETRY = ROOT / "reports" / "nimble" / "production-gate-latest.json"

LATEST_REGRESSION = ROOT / "reports" / "nimble" / "performance-regression-latest.json"

PROMOTION_REPORT = (
    ROOT / "reports" / "nimble" / "performance-baseline-promotion-latest.json"
)


def read_json(
    path: Path,
) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Required file is missing: {path.relative_to(ROOT)}")

    return json.loads(path.read_text(encoding="utf-8"))


def sha256(
    path: Path,
) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def build_metrics(
    telemetry: dict[str, Any],
) -> dict[str, float | int]:
    bundle = telemetry["bundle"]
    gate = telemetry["gate"]
    primary = bundle.get("primary")

    if primary is None:
        raise ValueError("Telemetry contains no primary bundle.")

    secondary = [chunk for chunk in bundle["chunks"] if chunk["kind"] == "secondary"]

    return {
        "primary_bundle_bytes": primary["bytes"],
        "secondary_chunk_count": bundle["secondary_chunk_count"],
        "total_javascript_bytes": sum(chunk["bytes"] for chunk in bundle["chunks"]),
        "largest_secondary_chunk_bytes": max(
            (chunk["bytes"] for chunk in secondary),
            default=0,
        ),
        "gate_duration_seconds": gate["duration_seconds"],
    }


def archive_current_baseline(
    baseline: dict[str, Any],
) -> Path:
    BASELINE_HISTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    created_at = str(
        baseline.get(
            "created_at",
            "unknown",
        )
    )

    safe_timestamp = created_at.replace(":", "-").replace("+", "_")

    source = baseline.get("source", {})
    short_commit = source.get(
        "short_commit",
        "unknown",
    )

    archive_path = BASELINE_HISTORY / (
        f"performance-baseline-{safe_timestamp}-{short_commit}.json"
    )

    if not archive_path.exists():
        shutil.copy2(
            CURRENT_BASELINE,
            archive_path,
        )

    return archive_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Promote current Nimble production telemetry "
            "to the governed performance baseline."
        )
    )

    parser.add_argument(
        "--rationale",
        required=True,
        help=(
            "Explicit architectural or product rationale "
            "for changing the performance baseline."
        ),
    )

    parser.add_argument(
        "--approved-by",
        required=True,
        help=("Person or governance body approving the baseline promotion."),
    )

    parser.add_argument(
        "--ticket",
        default=None,
        help=("Optional ticket, proposal, or decision record."),
    )

    parser.add_argument(
        "--allow-failed-regression",
        action="store_true",
        help=(
            "Permit promotion when the latest regression "
            "report is FAIL. This is recorded explicitly."
        ),
    )

    arguments = parser.parse_args()

    rationale = arguments.rationale.strip()
    approved_by = arguments.approved_by.strip()

    if len(rationale) < 20:
        print("FAIL: Promotion rationale must contain at least 20 characters.")
        return 1

    if not approved_by:
        print("FAIL: An approving person or body is required.")
        return 1

    current_baseline = read_json(CURRENT_BASELINE)
    telemetry = read_json(LATEST_TELEMETRY)
    regression = read_json(LATEST_REGRESSION)

    if telemetry["gate"]["status"] != "PASS":
        print("FAIL: The latest production gate did not pass.")
        return 1

    regression_status = regression["status"]

    if regression_status != "PASS" and not arguments.allow_failed_regression:
        print(
            "FAIL: Latest performance regression report "
            "is not PASS. Use --allow-failed-regression "
            "only for an explicitly approved exception."
        )
        return 1

    archive_path = archive_current_baseline(current_baseline)

    promoted_at = datetime.now(UTC).isoformat()

    new_baseline = {
        "schema_version": "1.1",
        "created_at": promoted_at,
        "source": {
            "commit": telemetry["git"]["commit"],
            "short_commit": telemetry["git"]["short_commit"],
            "branch": telemetry["git"]["branch"],
            "telemetry_generated_at": telemetry["generated_at"],
        },
        "metrics": build_metrics(telemetry),
        "thresholds": current_baseline["thresholds"],
        "promotion": {
            "rationale": rationale,
            "approved_by": approved_by,
            "ticket": arguments.ticket,
            "regression_status": regression_status,
            "failed_regression_override": bool(arguments.allow_failed_regression),
            "previous_baseline_sha256": sha256(CURRENT_BASELINE),
            "archived_baseline": str(archive_path.relative_to(ROOT)),
        },
    }

    CURRENT_BASELINE.write_text(
        json.dumps(
            new_baseline,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    promotion_record = {
        "schema_version": "1.0",
        "promoted_at": promoted_at,
        "status": "PROMOTED",
        "approved_by": approved_by,
        "rationale": rationale,
        "ticket": arguments.ticket,
        "previous_baseline": {
            "path": str(archive_path.relative_to(ROOT)),
            "sha256": new_baseline["promotion"]["previous_baseline_sha256"],
        },
        "new_baseline": {
            "path": str(CURRENT_BASELINE.relative_to(ROOT)),
            "sha256": sha256(CURRENT_BASELINE),
            "source_commit": telemetry["git"]["commit"],
            "metrics": new_baseline["metrics"],
        },
        "regression_status": regression_status,
        "failed_regression_override": bool(arguments.allow_failed_regression),
    }

    PROMOTION_REPORT.write_text(
        json.dumps(
            promotion_record,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ PERFORMANCE BASELINE PROMOTION")
    print("=" * 72)
    print(
        "Approved by:",
        approved_by,
    )
    print(
        "Rationale:",
        rationale,
    )
    print(
        "Previous baseline:",
        archive_path.relative_to(ROOT),
    )
    print(
        "New baseline:",
        CURRENT_BASELINE.relative_to(ROOT),
    )
    print(
        "Source commit:",
        telemetry["git"]["short_commit"],
    )
    print(
        "Regression status:",
        regression_status,
    )
    print("Status: PROMOTED")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
