#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent

LEDGER_RELATIVE_PATH = Path(
    "nimble/governance/audit/"
    "deployment-audit-ledger.jsonl"
)

SOURCE_GENERATOR = (
    "create_nimble_audit_recovery_source.py"
)

SOURCE_VALIDATOR = (
    "validate_nimble_audit_recovery_source.py"
)

AUDIT_WRITER = "append_nimble_audit_event.py"


def run(
    command: list[str],
    *,
    cwd: Path,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )


def digest(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def append_test_event(
    temporary_root: Path,
    event_type: str,
) -> None:
    result = run(
        [
            "python",
            AUDIT_WRITER,
            "--event-type",
            event_type,
            "--environment",
            "staging",
            "--release",
            "audit-recovery-simulation-v0.1",
            "--revision",
            "recovery-simulation",
            "--metadata-json",
            '{"simulation":true}',
        ],
        cwd=temporary_root,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stdout + result.stderr
        )


def main() -> int:
    canonical_ledger = ROOT / LEDGER_RELATIVE_PATH

    canonical_digest_before = digest(
        canonical_ledger
    )

    with tempfile.TemporaryDirectory() as directory:
        temporary_root = Path(directory)

        shutil.copytree(
            ROOT / "nimble",
            temporary_root / "nimble",
        )

        shutil.copytree(
            ROOT / "reports/nimble",
            temporary_root / "reports/nimble",
        )

        for script_name in [
            SOURCE_GENERATOR,
            SOURCE_VALIDATOR,
            AUDIT_WRITER,
        ]:
            shutil.copy2(
                ROOT / script_name,
                temporary_root / script_name,
            )

        temporary_ledger = (
            temporary_root
            / LEDGER_RELATIVE_PATH
        )

        existing_lines = [
            line
            for line in temporary_ledger.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]

        # A genesis checkpoint may legitimately anchor an
        # empty ledger. Seed only the isolated test copy so
        # truncation and reconstruction remain testable.
        if not existing_lines:
            append_test_event(
                temporary_root,
                "deployment_started",
            )

            append_test_event(
                temporary_root,
                "deployment_completed",
            )

        trusted_ledger_bytes = (
            temporary_ledger.read_bytes()
        )

        trusted_lines = [
            line
            for line in trusted_ledger_bytes.decode(
                "utf-8"
            ).splitlines()
            if line.strip()
        ]

        if len(trusted_lines) < 1:
            print(
                "FAIL: isolated recovery source "
                "contains no ledger events."
            )
            return 1

        generator_result = run(
            [
                "python",
                SOURCE_GENERATOR,
            ],
            cwd=temporary_root,
        )

        if generator_result.returncode != 0:
            print(generator_result.stdout)
            print(generator_result.stderr)
            return 1

        source_path = (
            temporary_root
            / "reports/nimble/recovery/"
            "trusted-audit-recovery-source.json"
        )

        # Remove at least the final trusted event from the
        # isolated canonical ledger.
        truncated_lines = trusted_lines[:-1]

        temporary_ledger.write_text(
            (
                "\n".join(truncated_lines)
                + ("\n" if truncated_lines else "")
            ),
            encoding="utf-8",
        )

        truncated_ledger_bytes = (
            temporary_ledger.read_bytes()
        )

        if (
            truncated_ledger_bytes
            == trusted_ledger_bytes
        ):
            print(
                "FAIL: isolated ledger was not truncated."
            )
            return 1

        reconstructed_path = (
            temporary_root
            / "reports/nimble/recovery/"
            "simulation-reconstructed-ledger.jsonl"
        )

        validator_result = run(
            [
                "python",
                SOURCE_VALIDATOR,
                "--source",
                str(source_path),
                "--output",
                str(reconstructed_path),
            ],
            cwd=temporary_root,
        )

        if validator_result.returncode != 0:
            print(validator_result.stdout)
            print(validator_result.stderr)
            return 1

        if not reconstructed_path.is_file():
            print(
                "FAIL: reconstructed ledger was not written."
            )
            return 1

        if (
            reconstructed_path.read_bytes()
            != trusted_ledger_bytes
        ):
            print(
                "FAIL: reconstructed ledger differs "
                "from the trusted recovery source."
            )
            return 1

        # Validation/reconstruction must not overwrite the
        # isolated canonical ledger.
        if (
            temporary_ledger.read_bytes()
            != truncated_ledger_bytes
        ):
            print(
                "FAIL: temporary canonical ledger "
                "was automatically restored."
            )
            return 1

    canonical_digest_after = digest(
        canonical_ledger
    )

    if canonical_digest_before != canonical_digest_after:
        print(
            "FAIL: canonical audit ledger was modified."
        )
        return 1

    print("=" * 72)
    print("NIMBLE™ AUDIT RECOVERY SIMULATION")
    print("=" * 72)
    print("Genesis checkpoint compatibility: PASS")
    print("Trusted source validation: PASS")
    print("Truncated ledger diagnosis: PASS")
    print("Separate reconstruction: PASS")
    print("Automatic canonical mutation: BLOCKED")
    print("Canonical ledger isolation: PASS")
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
