from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOW = (
    ROOT
    / ".github"
    / "workflows"
    / "nimble-production-gate.yml"
)

REQUIRED_MARKERS = (
    "name: Nimble Production Gate",
    "actions/checkout@v4",
    "actions/setup-python@v5",
    "actions/setup-node@v4",
    'node-version: "24"',
    "npm ci",
    "python validate_nimble_dependency_manifest.py",
    "python scan_nimble_dependency_risk.py",
    "python validate_nimble_dependency_risk.py",
    "tests/experience_gateway",
    "python collect_nimble_production_telemetry.py",
    "python validate_nimble_telemetry.py",
    "python validate_nimble_performance_regression.py",
    "python validate_nimble_baseline_governance.py",
    "python validate_nimble_release_attestation.py",
    "actions/upload-artifact@v4",
    "cancel-in-progress: true",
)


def main() -> int:
    if not WORKFLOW.exists():
        print(
            "FAIL: Nimble production workflow is missing."
        )
        return 1

    text = WORKFLOW.read_text(
        encoding="utf-8",
    )

    missing = [
        marker
        for marker in REQUIRED_MARKERS
        if marker not in text
    ]

    if missing:
        for marker in missing:
            print(
                "FAIL: Missing CI marker:",
                marker,
            )
        return 1

    print("=" * 72)
    print("NIMBLE™ CI VALIDATION")
    print("=" * 72)
    print("Workflow: present")
    print("Python runtime: configured")
    print("Node 24 runtime: configured")
    print("Deterministic npm install: configured")
    print("Gateway tests: configured")
    print("Production gate: configured")
    print("Build artifacts: retained")
    print("Concurrency control: active")
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
