#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

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


def git(*arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def canonical_json_bytes(
    payload: dict[str, Any],
) -> bytes:
    return (
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        )
        + "\n"
    ).encode("utf-8")


def subject_record(path: Path) -> dict[str, Any]:
    relative = path.relative_to(ROOT)

    return {
        "path": relative.as_posix(),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--release-ref",
        default=(
            os.environ.get("GITHUB_REF_NAME")
            or git("rev-parse", "--abbrev-ref", "HEAD")
        ),
    )

    parser.add_argument(
        "--release-version",
        default=(
            os.environ.get("NIMBLE_RELEASE_VERSION")
            or os.environ.get("GITHUB_REF_NAME")
            or git("rev-parse", "--short=12", "HEAD")
        ),
    )

    parser.add_argument(
        "--require-clean",
        action="store_true",
    )

    arguments = parser.parse_args()

    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    worktree_status = git("status", "--porcelain")

    if arguments.require_clean and worktree_status:
        raise RuntimeError(
            "Release manifest generation requires "
            "a clean Git worktree."
        )

    subjects: list[dict[str, Any]] = []

    missing_required: list[str] = []

    for relative_path in contract[
        "required_subjects"
    ]:
        path = ROOT / relative_path

        if not path.is_file():
            missing_required.append(relative_path)
            continue

        subjects.append(subject_record(path))

    if missing_required:
        raise RuntimeError(
            "Missing required release subjects: "
            + ", ".join(missing_required)
        )

    for relative_path in contract[
        "conditional_subjects"
    ]:
        path = ROOT / relative_path

        if path.is_file():
            subjects.append(subject_record(path))

    subjects.sort(
        key=lambda item: item["path"]
    )

    paths = [
        subject["path"]
        for subject in subjects
    ]

    if len(paths) != len(set(paths)):
        raise RuntimeError(
            "Duplicate release subjects detected."
        )

    revision = git("rev-parse", "HEAD")

    exact_tags = [
        tag
        for tag in git(
            "tag",
            "--points-at",
            revision,
        ).splitlines()
        if tag
    ]

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "manifest_id": "nimble-release-manifest-v0.1",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "release": {
            "name": "AletheusOS Nimble",
            "version": arguments.release_version,
            "ref": arguments.release_ref,
            "revision": revision,
            "tags": sorted(exact_tags),
            "repository": (
                os.environ.get(
                    "GITHUB_REPOSITORY"
                )
                or "local"
            ),
            "workflow_run_id": (
                os.environ.get(
                    "GITHUB_RUN_ID"
                )
            ),
            "workflow_run_attempt": (
                os.environ.get(
                    "GITHUB_RUN_ATTEMPT"
                )
            ),
        },
        "integrity": {
            "algorithm": "sha256",
            "subject_count": len(subjects),
            "worktree_clean": not bool(
                worktree_status
            ),
        },
        "subjects": subjects,
    }

    MANIFEST_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest_bytes = canonical_json_bytes(
        payload
    )

    MANIFEST_PATH.write_bytes(
        manifest_bytes
    )

    manifest_digest = hashlib.sha256(
        manifest_bytes
    ).hexdigest()

    CHECKSUM_PATH.write_text(
        f"{manifest_digest}  "
        f"{MANIFEST_PATH.name}\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ RELEASE MANIFEST")
    print("=" * 72)
    print(f"Revision: {revision}")
    print(f"Release ref: {arguments.release_ref}")
    print(f"Subjects: {len(subjects)}")
    print(f"SHA-256: {manifest_digest}")
    print(
        "Manifest:",
        MANIFEST_PATH.relative_to(ROOT),
    )
    print(
        "Checksum:",
        CHECKSUM_PATH.relative_to(ROOT),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
