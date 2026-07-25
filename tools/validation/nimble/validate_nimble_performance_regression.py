from __future__ import annotations

import json
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
LATEST_REGRESSION_JSON = (
    ROOT
    / "reports"
    / "nimble"
    / "performance-regression-latest.json"
)
LATEST_REGRESSION_MARKDOWN = (
    ROOT
    / "reports"
    / "nimble"
    / "performance-regression-latest.md"
)


def percent_change(
    current: float,
    baseline: float,
) -> float:
    if baseline == 0:
        return 0.0 if current == 0 else 100.0

    return (
        (current - baseline)
        / baseline
        * 100.0
    )


def metric_result(
    *,
    name: str,
    current: float,
    baseline: float,
    allowed_growth_percent: float | None = None,
    absolute_limit: float | None = None,
) -> dict[str, Any]:
    growth = percent_change(
        current,
        baseline,
    )

    failures: list[str] = []

    if (
        allowed_growth_percent is not None
        and growth > allowed_growth_percent
    ):
        failures.append(
            f"growth {growth:.2f}% exceeds "
            f"{allowed_growth_percent:.2f}%"
        )

    if (
        absolute_limit is not None
        and current > absolute_limit
    ):
        failures.append(
            f"value {current:.2f} exceeds "
            f"absolute limit {absolute_limit:.2f}"
        )

    return {
        "name": name,
        "baseline": baseline,
        "current": current,
        "change": current - baseline,
        "change_percent": round(growth, 4),
        "allowed_growth_percent":
            allowed_growth_percent,
        "absolute_limit": absolute_limit,
        "status": (
            "PASS"
            if not failures
            else "FAIL"
        ),
        "failures": failures,
    }


def write_markdown(
    result: dict[str, Any],
) -> None:
    lines = [
        "# Nimble Performance Regression Report",
        "",
        f"Status: **{result['status']}**",
        "",
        f"Baseline commit: `{result['baseline_source']['short_commit']}`",
        f"Current commit: `{result['current_source']['short_commit']}`",
        "",
        "## Metrics",
        "",
        "| Metric | Baseline | Current | Change | Change % | Status |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for metric in result["metrics"]:
        lines.append(
            f"| {metric['name']} "
            f"| {metric['baseline']:.2f} "
            f"| {metric['current']:.2f} "
            f"| {metric['change']:.2f} "
            f"| {metric['change_percent']:.2f}% "
            f"| **{metric['status']}** |"
        )

    chunk = result["chunk_count"]

    lines.extend(
        [
            "",
            "## Chunk structure",
            "",
            f"- Baseline secondary chunks: `{chunk['baseline']}`",
            f"- Current secondary chunks: `{chunk['current']}`",
            f"- Change: `{chunk['change']}`",
            f"- Status: **{chunk['status']}**",
        ]
    )

    if result["failures"]:
        lines.extend(
            [
                "",
                "## Failures",
                "",
            ]
        )

        for failure in result["failures"]:
            lines.append(f"- {failure}")

    LATEST_REGRESSION_MARKDOWN.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    if not LATEST_REPORT.exists():
        print(
            "FAIL: Current production telemetry is missing."
        )
        return 1

    if not BASELINE_PATH.exists():
        print(
            "FAIL: Performance baseline is missing."
        )
        return 1

    report: dict[str, Any] = json.loads(
        LATEST_REPORT.read_text(encoding="utf-8")
    )

    baseline: dict[str, Any] = json.loads(
        BASELINE_PATH.read_text(encoding="utf-8")
    )

    bundle = report["bundle"]
    gate = report["gate"]
    thresholds = baseline["thresholds"]
    baseline_metrics = baseline["metrics"]

    primary = bundle.get("primary")

    if primary is None:
        print(
            "FAIL: Current report has no primary bundle."
        )
        return 1

    secondary_chunks = [
        chunk
        for chunk in bundle["chunks"]
        if chunk["kind"] == "secondary"
    ]

    current_metrics = {
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
    }

    metric_results = [
        metric_result(
            name="Primary bundle bytes",
            current=current_metrics[
                "primary_bundle_bytes"
            ],
            baseline=baseline_metrics[
                "primary_bundle_bytes"
            ],
            allowed_growth_percent=thresholds[
                "primary_bundle_growth_percent"
            ],
            absolute_limit=thresholds[
                "primary_bundle_absolute_limit_bytes"
            ],
        ),
        metric_result(
            name="Total JavaScript bytes",
            current=current_metrics[
                "total_javascript_bytes"
            ],
            baseline=baseline_metrics[
                "total_javascript_bytes"
            ],
            allowed_growth_percent=thresholds[
                "total_javascript_growth_percent"
            ],
        ),
        metric_result(
            name="Largest secondary chunk bytes",
            current=current_metrics[
                "largest_secondary_chunk_bytes"
            ],
            baseline=baseline_metrics[
                "largest_secondary_chunk_bytes"
            ],
            allowed_growth_percent=thresholds[
                "largest_secondary_growth_percent"
            ],
        ),
        metric_result(
            name="Production gate duration seconds",
            current=current_metrics[
                "gate_duration_seconds"
            ],
            baseline=baseline_metrics[
                "gate_duration_seconds"
            ],
            allowed_growth_percent=thresholds[
                "gate_duration_growth_percent"
            ],
            absolute_limit=thresholds[
                "gate_duration_absolute_limit_seconds"
            ],
        ),
    ]

    baseline_chunks = baseline_metrics[
        "secondary_chunk_count"
    ]
    current_chunks = current_metrics[
        "secondary_chunk_count"
    ]
    chunk_change = (
        current_chunks - baseline_chunks
    )

    minimum_chunks = (
        baseline_chunks
        - thresholds[
            "secondary_chunk_count_decrease_allowed"
        ]
    )

    maximum_chunks = (
        baseline_chunks
        + thresholds[
            "secondary_chunk_count_increase_allowed"
        ]
    )

    chunk_status = (
        "PASS"
        if minimum_chunks
        <= current_chunks
        <= maximum_chunks
        else "FAIL"
    )

    failures: list[str] = []

    for metric in metric_results:
        for failure in metric["failures"]:
            failures.append(
                f"{metric['name']}: {failure}"
            )

    if chunk_status == "FAIL":
        failures.append(
            "Secondary chunk count "
            f"{current_chunks} is outside "
            f"the permitted range "
            f"{minimum_chunks}–{maximum_chunks}."
        )

    result = {
        "schema_version": "1.0",
        "status": (
            "PASS"
            if not failures
            else "FAIL"
        ),
        "baseline_source": baseline["source"],
        "current_source": report["git"],
        "metrics": metric_results,
        "chunk_count": {
            "baseline": baseline_chunks,
            "current": current_chunks,
            "change": chunk_change,
            "minimum": minimum_chunks,
            "maximum": maximum_chunks,
            "status": chunk_status,
        },
        "failures": failures,
    }

    LATEST_REGRESSION_JSON.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    LATEST_REGRESSION_JSON.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    write_markdown(result)

    print("=" * 72)
    print("NIMBLE™ PERFORMANCE REGRESSION GOVERNANCE")
    print("=" * 72)

    for metric in metric_results:
        print(
            f"{metric['name']}: "
            f"{metric['current']:.2f} "
            f"({metric['change_percent']:+.2f}%) "
            f"{metric['status']}"
        )

    print(
        "Secondary chunks:",
        current_chunks,
        f"({chunk_change:+d})",
        chunk_status,
    )

    if failures:
        print()
        for failure in failures:
            print("FAIL:", failure)

    print("Status:", result["status"])

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
