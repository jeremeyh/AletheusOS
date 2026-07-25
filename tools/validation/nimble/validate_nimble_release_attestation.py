from __future__ import annotations

import hashlib
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


LATEST_ATTESTATION = (
    ROOT
    / "reports"
    / "nimble"
    / "release-attestation-latest.json"
)

REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "release",
    "source",
    "runtime",
    "evidence",
    "validators",
    "artifacts",
    "attestation_sha256",
}


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


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> int:
    if not LATEST_ATTESTATION.exists():
        print(
            "FAIL: Release attestation is missing."
        )
        return 1

    attestation: dict[str, Any] = json.loads(
        LATEST_ATTESTATION.read_text(
            encoding="utf-8",
        )
    )

    missing = (
        REQUIRED_TOP_LEVEL_KEYS
        - set(attestation)
    )

    if missing:
        print(
            "FAIL: Missing attestation keys:",
            ", ".join(sorted(missing)),
        )
        return 1

    expected_digest = attestation[
        "attestation_sha256"
    ]

    unsigned = {
        key: value
        for key, value in attestation.items()
        if key != "attestation_sha256"
    }

    actual_digest = canonical_digest(
        unsigned
    )

    if actual_digest != expected_digest:
        print(
            "FAIL: Attestation digest mismatch."
        )
        return 1

    if not attestation["source"][
        "working_tree_clean"
    ]:
        print(
            "FAIL: Attested working tree was not clean."
        )
        return 1

    validator_failures = [
        item
        for item in attestation["validators"]
        if item["status"] != "PASS"
    ]

    if validator_failures:
        for failure in validator_failures:
            print(
                "FAIL: Validator did not pass:",
                failure["validator"],
            )
        return 1

    for evidence in attestation[
        "evidence"
    ].values():
        path = ROOT / evidence["path"]

        if not path.exists():
            print(
                "FAIL: Evidence file is missing:",
                evidence["path"],
            )
            return 1

        if sha256_file(path) != evidence["sha256"]:
            print(
                "FAIL: Evidence hash mismatch:",
                evidence["path"],
            )
            return 1

    artifact = attestation[
        "artifacts"
    ][
        "platform_shell_dist"
    ]

    for file_record in artifact["files"]:
        path = ROOT / file_record["path"]

        if not path.exists():
            print(
                "FAIL: Attested artifact is missing:",
                file_record["path"],
            )
            return 1

        if (
            sha256_file(path)
            != file_record["sha256"]
        ):
            print(
                "FAIL: Artifact hash mismatch:",
                file_record["path"],
            )
            return 1

    print("=" * 72)
    print("NIMBLE™ RELEASE ATTESTATION VALIDATION")
    print("=" * 72)
    print(
        "Release:",
        attestation["release"]["identifier"],
    )
    print(
        "Commit:",
        attestation["source"]["short_commit"],
    )
    print(
        "Approved by:",
        attestation["release"]["approved_by"],
    )
    print(
        "Validators:",
        len(attestation["validators"]),
    )
    print(
        "Artifact files:",
        artifact["file_count"],
    )
    print("Evidence hashes: valid")
    print("Artifact hashes: valid")
    print("Attestation digest: valid")
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
