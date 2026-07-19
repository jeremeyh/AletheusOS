from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

PRODUCTION_EVIDENCE = (
    ROOT
    / "reports"
    / "nimble"
    / "production-gate-latest.json"
)

PERFORMANCE_REPORT = (
    ROOT
    / "reports"
    / "nimble"
    / "performance-regression-latest.json"
)

PERFORMANCE_BASELINE = (
    ROOT
    / "nimble"
    / "governance"
    / "performance-baseline.json"
)

LATEST_ATTESTATION = (
    ROOT
    / "reports"
    / "nimble"
    / "release-attestation-latest.json"
)

ATTESTATION_ARCHIVE = (
    ROOT
    / "nimble"
    / "governance"
    / "attestations"
)

DIST_DIRECTORY = (
    ROOT
    / "nimble"
    / "apps"
    / "platform-shell"
    / "dist"
)

REQUIRED_VALIDATORS = (
    "validate_nimble_foundation.py",
    "validate_nimble_tokens.py",
    "validate_nimble_components.py",
    "validate_nimble_reference_shell.py",
    "validate_nimble_bundle_boundary.py",
    "validate_nimble_route_splitting.py",
    "validate_nimble_telemetry.py",
    "validate_nimble_performance_regression.py",
    "validate_nimble_baseline_governance.py",
    "validate_nimble_ci.py",
)


def run(
    command: list[str],
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=dict(os.environ),
        )
    except FileNotFoundError as error:
        return subprocess.CompletedProcess(
            args=command,
            returncode=127,
            stdout=str(error),
            stderr=None,
        )


def command_output(
    command: list[str],
    fallback: str = "unknown",
) -> str:
    completed = run(command)

    if completed.returncode != 0:
        return fallback

    value = completed.stdout.strip()
    return value or fallback


def load_json(
    path: Path,
) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(
            f"Required evidence is missing: "
            f"{path.relative_to(ROOT)}"
        )

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def hash_directory(
    directory: Path,
) -> dict[str, Any]:
    files: list[dict[str, Any]] = []

    if not directory.exists():
        return {
            "path": str(
                directory.relative_to(ROOT)
            ),
            "files": [],
            "file_count": 0,
            "aggregate_sha256": None,
        }

    aggregate = hashlib.sha256()

    for path in sorted(
        item
        for item in directory.rglob("*")
        if item.is_file()
    ):
        relative = path.relative_to(ROOT)
        digest = sha256_file(path)

        aggregate.update(
            str(relative).encode("utf-8")
        )
        aggregate.update(digest.encode("ascii"))

        files.append(
            {
                "path": str(relative),
                "bytes": path.stat().st_size,
                "sha256": digest,
            }
        )

    return {
        "path": str(
            directory.relative_to(ROOT)
        ),
        "files": files,
        "file_count": len(files),
        "aggregate_sha256":
            aggregate.hexdigest(),
    }


def run_validators() -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    for filename in REQUIRED_VALIDATORS:
        path = ROOT / filename

        if not path.exists():
            results.append(
                {
                    "validator": filename,
                    "status": "MISSING",
                    "exit_code": None,
                    "output": "",
                }
            )
            continue

        completed = run(
            [
                sys.executable,
                filename,
            ]
        )

        results.append(
            {
                "validator": filename,
                "status": (
                    "PASS"
                    if completed.returncode == 0
                    else "FAIL"
                ),
                "exit_code":
                    completed.returncode,
                "output":
                    completed.stdout,
            }
        )

    return results


def canonical_digest(
    value: dict[str, Any],
) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")

    return hashlib.sha256(
        payload
    ).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a durable Nimble release attestation."
        )
    )

    parser.add_argument(
        "--release",
        required=True,
        help=(
            "Release identifier, for example "
            "nimble-v0.1.0 or Genesis-8-Nimble-1."
        ),
    )

    parser.add_argument(
        "--approved-by",
        required=True,
        help=(
            "Approving person or governance body."
        ),
    )

    parser.add_argument(
        "--notes",
        default="",
        help=(
            "Optional release notes or decision context."
        ),
    )

    arguments = parser.parse_args()

    production = load_json(
        PRODUCTION_EVIDENCE
    )

    performance = load_json(
        PERFORMANCE_REPORT
    )

    baseline = load_json(
        PERFORMANCE_BASELINE
    )

    validator_results = run_validators()

    validator_failures = [
        result
        for result in validator_results
        if result["status"] != "PASS"
    ]

    if production["gate"]["status"] != "PASS":
        print(
            "FAIL: Production gate evidence is not PASS."
        )
        return 1

    if performance["status"] != "PASS":
        print(
            "FAIL: Performance regression evidence "
            "is not PASS."
        )
        return 1

    if validator_failures:
        for result in validator_failures:
            print(
                "FAIL:",
                result["validator"],
                result["status"],
            )
        return 1

    commit = command_output(
        [
            "git",
            "rev-parse",
            "HEAD",
        ]
    )

    short_commit = command_output(
        [
            "git",
            "rev-parse",
            "--short",
            "HEAD",
        ]
    )

    branch = command_output(
        [
            "git",
            "branch",
            "--show-current",
        ]
    )

    dirty_output = command_output(
        [
            "git",
            "status",
            "--porcelain",
        ],
        fallback="",
    )

    if dirty_output:
        print(
            "FAIL: Release attestation requires "
            "a clean working tree."
        )
        return 1

    release = arguments.release.strip()
    approved_by = arguments.approved_by.strip()

    if not release:
        print(
            "FAIL: Release identifier is required."
        )
        return 1

    if not approved_by:
        print(
            "FAIL: Release approval is required."
        )
        return 1

    generated_at = datetime.now(
        timezone.utc
    ).isoformat()

    attestation: dict[str, Any] = {
        "schema_version": "1.0",
        "release": {
            "identifier": release,
            "generated_at": generated_at,
            "approved_by": approved_by,
            "notes": arguments.notes.strip(),
        },
        "source": {
            "commit": commit,
            "short_commit": short_commit,
            "branch": branch,
            "tags_at_head": [
                line
                for line in command_output(
                    [
                        "git",
                        "tag",
                        "--points-at",
                        "HEAD",
                    ],
                    fallback="",
                ).splitlines()
                if line
            ],
            "working_tree_clean": True,
        },
        "runtime": {
            "python":
                platform.python_version(),
            "python_executable":
                sys.executable,
            "platform":
                platform.platform(),
            "node":
                production["runtime"]["node"],
            "npm":
                production["runtime"]["npm"],
        },
        "evidence": {
            "production_gate": {
                "path": str(
                    PRODUCTION_EVIDENCE.relative_to(
                        ROOT
                    )
                ),
                "sha256":
                    sha256_file(
                        PRODUCTION_EVIDENCE
                    ),
                "status":
                    production["gate"]["status"],
            },
            "performance_regression": {
                "path": str(
                    PERFORMANCE_REPORT.relative_to(
                        ROOT
                    )
                ),
                "sha256":
                    sha256_file(
                        PERFORMANCE_REPORT
                    ),
                "status":
                    performance["status"],
            },
            "performance_baseline": {
                "path": str(
                    PERFORMANCE_BASELINE.relative_to(
                        ROOT
                    )
                ),
                "sha256":
                    sha256_file(
                        PERFORMANCE_BASELINE
                    ),
                "source_commit":
                    baseline["source"][
                        "short_commit"
                    ],
            },
        },
        "validators": validator_results,
        "artifacts": {
            "platform_shell_dist":
                hash_directory(
                    DIST_DIRECTORY
                ),
        },
    }

    attestation["attestation_sha256"] = (
        canonical_digest(attestation)
    )

    ATTESTATION_ARCHIVE.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_release = "".join(
        character
        if character.isalnum()
        or character in {"-", "_", "."}
        else "-"
        for character in release
    )

    archive_path = (
        ATTESTATION_ARCHIVE
        / (
            f"{safe_release}-"
            f"{short_commit}.json"
        )
    )

    serialized = (
        json.dumps(
            attestation,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    LATEST_ATTESTATION.write_text(
        serialized,
        encoding="utf-8",
    )

    archive_path.write_text(
        serialized,
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ RELEASE ATTESTATION")
    print("=" * 72)
    print("Release:", release)
    print("Commit:", short_commit)
    print("Approved by:", approved_by)
    print(
        "Validators:",
        len(validator_results),
    )
    print(
        "Artifact files:",
        attestation[
            "artifacts"
        ][
            "platform_shell_dist"
        ][
            "file_count"
        ],
    )
    print(
        "Attestation SHA-256:",
        attestation[
            "attestation_sha256"
        ],
    )
    print(
        "Latest:",
        LATEST_ATTESTATION.relative_to(ROOT),
    )
    print(
        "Archive:",
        archive_path.relative_to(ROOT),
    )
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
