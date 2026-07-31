from __future__ import annotations

from pathlib import Path


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)


WORKFLOW = ROOT / ".github" / "workflows" / "nimble-attested-release.yml"

REQUIRED_MARKERS = (
    "name: Nimble Attested Release",
    "tags:",
    '"nimble-*"',
    "actions/checkout@v4",
    "fetch-depth: 0",
    "actions/setup-python@v5",
    "actions/setup-node@v4",
    'node-version: "24"',
    "npm ci",
    "npm run build",
    "python validate_nimble_release_attestation.py",
    "Attestation commit matches tagged release parent",
    "actions/upload-artifact@v4",
    "reports/nimble/release-attestation-latest.json",
    "nimble/governance/attestations",
)


def main() -> int:
    if not WORKFLOW.exists():
        print("FAIL: Attested release workflow is missing.")
        return 1

    text = WORKFLOW.read_text(
        encoding="utf-8",
    )

    missing = [marker for marker in REQUIRED_MARKERS if marker not in text]

    if missing:
        for marker in missing:
            print(
                "FAIL: Missing release marker:",
                marker,
            )
        return 1

    print("=" * 72)
    print("NIMBLE™ ATTESTED RELEASE VALIDATION")
    print("=" * 72)
    print("Tag trigger: configured")
    print("Tagged commit verification: configured")
    print("Deterministic rebuild: configured")
    print("Evidence validation: configured")
    print("Attestation validation: configured")
    print("Commit binding: configured")
    print("Release artifact retention: configured")
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
