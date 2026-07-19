#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent

CANONICAL_LEDGER = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger.jsonl"
)

WRITER = ROOT / "append_nimble_audit_event.py"
VALIDATOR = ROOT / "validate_nimble_audit_ledger.py"


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
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)

        shutil.copytree(
            ROOT / "nimble",
            temporary_root / "nimble",
        )

        shutil.copy2(
            WRITER,
            temporary_root / WRITER.name,
        )

        shutil.copy2(
            VALIDATOR,
            temporary_root / VALIDATOR.name,
        )

        temporary_ledger = (
            temporary_root
            / "nimble/governance/audit/"
            "deployment-audit-ledger.jsonl"
        )

        temporary_ledger.write_text(
            "",
            encoding="utf-8",
        )

        first = run(
            [
                "python",
                WRITER.name,
                "--event-type",
                "deployment_started",
                "--environment",
                "staging",
                "--release",
                "tamper-test-v1",
                "--revision",
                "abc123",
                "--metadata-json",
                '{"status":"started"}',
            ],
            cwd=temporary_root,
        )

        if first.returncode != 0:
            print(first.stdout)
            print(first.stderr)
            return 1

        second = run(
            [
                "python",
                WRITER.name,
                "--event-type",
                "deployment_completed",
                "--environment",
                "staging",
                "--release",
                "tamper-test-v1",
                "--revision",
                "abc123",
                "--metadata-json",
                '{"status":"completed"}',
            ],
            cwd=temporary_root,
        )

        if second.returncode != 0:
            print(second.stdout)
            print(second.stderr)
            return 1

        valid_result = run(
            [
                "python",
                VALIDATOR.name,
            ],
            cwd=temporary_root,
        )

        if valid_result.returncode != 0:
            print(
                "FAIL: untampered temporary ledger "
                "did not validate."
            )
            print(valid_result.stdout)
            print(valid_result.stderr)
            return 1

        lines = temporary_ledger.read_text(
            encoding="utf-8",
        ).splitlines()

        first_event = json.loads(lines[0])

        first_event["release"] = "tampered-release"

        lines[0] = json.dumps(
            first_event,
            sort_keys=True,
            separators=(",", ":"),
        )

        temporary_ledger.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )

        tampered_result = run(
            [
                "python",
                VALIDATOR.name,
            ],
            cwd=temporary_root,
        )

        if tampered_result.returncode == 0:
            print(
                "FAIL: tampered ledger unexpectedly passed."
            )
            return 1

        output = (
            tampered_result.stdout
            + tampered_result.stderr
        )

        if "event_hash mismatch" not in output:
            print(
                "FAIL: tamper was rejected, but the "
                "expected hash mismatch was not reported."
            )
            print(output)
            return 1

        canonical_contents = (
            CANONICAL_LEDGER.read_text(
                encoding="utf-8",
            )
            if CANONICAL_LEDGER.exists()
            else ""
        )

        if "tamper-test-v1" in canonical_contents:
            print(
                "FAIL: canonical ledger was modified "
                "during the tamper test."
            )
            return 1

        print("=" * 72)
        print("NIMBLE™ AUDIT LEDGER TAMPER TEST")
        print("=" * 72)
        print("Untampered temporary ledger: PASS")
        print("Historical event modification: DETECTED")
        print("Canonical ledger isolation: PASS")
        print("Status: PASS")

        return 0


if __name__ == "__main__":
    raise SystemExit(main())
