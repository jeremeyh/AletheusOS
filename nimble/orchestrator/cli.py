from __future__ import annotations

import argparse
from pathlib import Path

from .report import generate_report


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect AletheusOS build readiness "
            "without mutating source code."
        )
    )

    parser.add_argument(
        "--root",
        default=".",
    )

    parser.add_argument(
        "--report",
        default=(
            "reports/nimble/orchestrator/"
            "build-state-latest.json"
        ),
    )

    arguments = parser.parse_args()

    root = Path(
        arguments.root
    ).resolve()

    report_path = Path(
        arguments.report
    )

    if not report_path.is_absolute():
        report_path = (
            root / report_path
        )

    report = generate_report(
        root,
        report_path,
    )

    print("=" * 72)
    print("NIMBLE™ BUILD ORCHESTRATOR")
    print("=" * 72)
    print(
        "Overall readiness:",
        f"{report['overall_readiness_percent']}%",
    )

    summary = report["summary"]

    print(
        "Implemented:",
        summary["implemented"],
    )
    print(
        "Partial:",
        summary["partial"],
    )
    print(
        "Blocked:",
        summary["blocked"],
    )
    print(
        "Missing:",
        summary["missing"],
    )
    print(
        "Drift findings:",
        summary["drift_findings"],
    )

    print()
    print("Capability state:")

    for capability in report[
        "capabilities"
    ]:
        print(
            f"- {capability['display_name']}: "
            f"{capability['state']} "
            f"({capability['readiness_percent']}%)"
        )

        if capability["blocked_by"]:
            print(
                "  blocked by:",
                ", ".join(
                    capability[
                        "blocked_by"
                    ]
                ),
            )

    print()
    print("Recommended build plan:")

    if not report["build_plan"]:
        print("- No remaining build work.")
    else:
        for item in report[
            "build_plan"
        ]:
            print(
                f"- {item['display_name']}: "
                f"{item['action']} "
                f"({item['reason']})"
            )

    print()
    print(
        "Report:",
        report_path.relative_to(root),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
