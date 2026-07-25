#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
import subprocess
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


CONTRACT_PATH = (
    ROOT
    / "nimble/governance/release/"
    "release-integrity-contract.json"
)

MANIFEST_PATH = (
    ROOT
    / "reports/nimble/"
    "nimble-release-manifest.json"
)

CHECKSUM_PATH = (
    ROOT
    / "reports/nimble/"
    "nimble-release-manifest.sha256"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "release-integrity-latest.json"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def write_report(
    payload: dict[str, Any],
) -> None:
    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    if not CONTRACT_PATH.is_file():
        failures.append(
            "Release-integrity contract is missing."
        )

    if not MANIFEST_PATH.is_file():
        failures.append(
            "Release manifest is missing."
        )

    if not CHECKSUM_PATH.is_file():
        failures.append(
            "Release-manifest checksum is missing."
        )

    if failures:
        report = {
            "schema_version": "1.0",
            "generated_at": datetime.now(
                UTC
            ).isoformat(),
            "status": "FAIL",
            "checks": checks,
            "failures": failures,
        }

        write_report(report)

        for failure in failures:
            print(f"- {failure}")

        return 1

    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    manifest = json.loads(
        MANIFEST_PATH.read_text(
            encoding="utf-8",
        )
    )

    checksum_line = CHECKSUM_PATH.read_text(
        encoding="utf-8",
    ).strip()

    match = re.fullmatch(
        r"([a-f0-9]{64})\s{2}"
        r"nimble-release-manifest\.json",
        checksum_line,
    )

    if match is None:
        failures.append(
            "Manifest checksum file has an invalid format."
        )
        expected_manifest_digest = ""
    else:
        expected_manifest_digest = match.group(1)

    actual_manifest_digest = sha256_file(
        MANIFEST_PATH
    )

    digest_matches = (
        expected_manifest_digest
        == actual_manifest_digest
    )

    checks.append(
        {
            "check": "manifest-checksum",
            "status": (
                "PASS"
                if digest_matches
                else "FAIL"
            ),
            "actual": actual_manifest_digest,
            "expected": expected_manifest_digest,
        }
    )

    if not digest_matches:
        failures.append(
            "Release-manifest checksum mismatch."
        )

    subjects = manifest.get("subjects", [])

    seen_paths: set[str] = set()

    for subject in subjects:
        relative_path = subject.get("path", "")
        expected_digest = subject.get(
            "sha256",
            "",
        )

        if not isinstance(relative_path, str):
            failures.append(
                "Release subject has a non-string path."
            )
            continue

        if relative_path.startswith("/"):
            failures.append(
                f"Absolute subject path forbidden: "
                f"{relative_path}"
            )
            continue

        if relative_path in seen_paths:
            failures.append(
                f"Duplicate subject: {relative_path}"
            )
            continue

        seen_paths.add(relative_path)

        path = ROOT / relative_path

        if not path.is_file():
            failures.append(
                f"Release subject is missing: "
                f"{relative_path}"
            )
            continue

        actual_digest = sha256_file(path)

        passed = actual_digest == expected_digest

        checks.append(
            {
                "check": (
                    f"subject-checksum:{relative_path}"
                ),
                "status": (
                    "PASS"
                    if passed
                    else "FAIL"
                ),
                "actual": actual_digest,
                "expected": expected_digest,
            }
        )

        if not passed:
            failures.append(
                f"Subject checksum mismatch: "
                f"{relative_path}"
            )

    required_subjects = set(
        contract["required_subjects"]
    )

    missing_required = sorted(
        required_subjects - seen_paths
    )

    for missing in missing_required:
        failures.append(
            f"Required subject missing from manifest: "
            f"{missing}"
        )

    revision = manifest.get(
        "release",
        {},
    ).get("revision")

    current_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    revision_matches = revision == current_revision

    checks.append(
        {
            "check": "git-revision",
            "status": (
                "PASS"
                if revision_matches
                else "FAIL"
            ),
            "manifest": revision,
            "current": current_revision,
        }
    )

    if not revision_matches:
        failures.append(
            "Manifest revision does not match HEAD."
        )

    status = "PASS" if not failures else "FAIL"

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            UTC
        ).isoformat(),
        "status": status,
        "manifest_sha256": (
            actual_manifest_digest
        ),
        "subject_count": len(subjects),
        "checks": checks,
        "failures": failures,
    }

    write_report(report)

    print("=" * 72)
    print("NIMBLE™ RELEASE INTEGRITY")
    print("=" * 72)
    print(f"Revision: {current_revision}")
    print(f"Subjects: {len(subjects)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
