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


REPORT = ROOT / "reports" / "nimble" / "dependency-risk-latest.json"

POLICY = ROOT / "nimble" / "governance" / "supply-chain" / "dependency-policy.json"

REQUIRED_KEYS = {
    "schema_version",
    "generated_at",
    "status",
    "policy",
    "manifest",
    "licenses",
    "npm_audit",
    "python_audit",
    "failures",
}


def main() -> int:
    if not POLICY.exists():
        print("FAIL: Dependency policy is missing.")
        return 1

    if not REPORT.exists():
        print("FAIL: Dependency risk report is missing.")
        return 1

    report: dict[str, Any] = json.loads(REPORT.read_text(encoding="utf-8"))

    missing = REQUIRED_KEYS - set(report)

    if missing:
        print(
            "FAIL: Missing risk report keys:",
            ", ".join(sorted(missing)),
        )
        return 1

    if report["status"] not in {
        "PASS",
        "FAIL",
    }:
        print("FAIL: Invalid dependency risk status.")
        return 1

    denied = report["licenses"]["denied"]

    if denied and report["status"] != "FAIL":
        print("FAIL: Denied licenses did not fail governance.")
        return 1

    if report["failures"] and report["status"] != "FAIL":
        print("FAIL: Risk failures exist but status is not FAIL.")
        return 1

    print("=" * 72)
    print("NIMBLE™ DEPENDENCY RISK VALIDATION")
    print("=" * 72)
    print(
        "Status:",
        report["status"],
    )
    print(
        "Allowed licenses:",
        len(report["licenses"]["allowed"]),
    )
    print(
        "Review required:",
        len(report["licenses"]["review_required"]),
    )
    print(
        "Denied licenses:",
        len(report["licenses"]["denied"]),
    )
    print(
        "npm audit available:",
        report["npm_audit"]["available"],
    )
    print(
        "pip-audit available:",
        report["python_audit"]["available"],
    )

    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
