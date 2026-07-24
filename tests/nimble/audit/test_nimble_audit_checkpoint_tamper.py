#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

WRITER = ROOT / "bin/append_nimble_audit_event.py"
CHECKPOINT_CREATOR = ROOT / "bin/create_nimble_audit_checkpoint.py"
CHECKPOINT_VALIDATOR = ROOT / "bin/validate_nimble_audit_checkpoints.py"


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
        timeout=30,
        env={
            **os.environ,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_EDITOR": "true",
            "GIT_SEQUENCE_EDITOR": "true",
        },
    )


def copy_runtime(temporary_root: Path) -> None:
    shutil.copytree(
        ROOT / "nimble",
        temporary_root / "nimble",
    )

    for source in [
        WRITER,
        CHECKPOINT_CREATOR,
        CHECKPOINT_VALIDATOR,
    ]:
        shutil.copy2(
            source,
            temporary_root / source.name,
        )

    git_commands = [
        ["git", "init"],
        [
            "git",
            "config",
            "user.name",
            "Nimble Audit Test",
        ],
        [
            "git",
            "config",
            "user.email",
            "nimble-audit-test@example.invalid",
        ],
        [
            "git",
            "config",
            "commit.gpgsign",
            "false",
        ],
        [
            "git",
            "config",
            "tag.gpgsign",
            "false",
        ],
        ["git", "add", "."],
        [
            "git",
            "commit",
            "--no-gpg-sign",
            "--no-verify",
            "-m",
            "Initialize isolated checkpoint test",
        ],
    ]

    for command in git_commands:
        result = run(
            command,
            cwd=temporary_root,
        )

        if result.returncode != 0:
            raise RuntimeError(
                "Temporary Git initialization failed: "
                + result.stdout
                + result.stderr
            )


def append_event(
    temporary_root: Path,
    event_type: str,
) -> None:
    result = run(
        [
            "python",
            WRITER.name,
            "--event-type",
            event_type,
            "--environment",
            "staging",
            "--release",
            "checkpoint-test-v1",
            "--revision",
            "abc123",
            "--metadata-json",
            '{"status":"test"}',
        ],
        cwd=temporary_root,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stdout + result.stderr
        )


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_root = Path(temporary_directory)

        copy_runtime(temporary_root)

        ledger_path = (
            temporary_root
            / "nimble/governance/audit/"
            "deployment-audit-ledger.jsonl"
        )

        checkpoint_directory = (
            temporary_root
            / "nimble/governance/audit/checkpoints"
        )

        ledger_path.write_text(
            "",
            encoding="utf-8",
        )

        if checkpoint_directory.exists():
            shutil.rmtree(checkpoint_directory)

        checkpoint_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        append_event(
            temporary_root,
            "deployment_started",
        )

        append_event(
            temporary_root,
            "deployment_completed",
        )

        checkpoint_result = run(
            [
                "python",
                CHECKPOINT_CREATOR.name,
                "--release",
                "checkpoint-test-v1",
            ],
            cwd=temporary_root,
        )

        if checkpoint_result.returncode != 0:
            print(checkpoint_result.stdout)
            print(checkpoint_result.stderr)
            return 1

        valid_result = run(
            [
                "python",
                CHECKPOINT_VALIDATOR.name,
            ],
            cwd=temporary_root,
        )

        if valid_result.returncode != 0:
            print(
                "FAIL: valid checkpoint chain did not validate."
            )
            print(valid_result.stdout)
            print(valid_result.stderr)
            return 1

        original_ledger = ledger_path.read_text(
            encoding="utf-8"
        )

        ledger_lines = original_ledger.splitlines()

        ledger_path.write_text(
            ledger_lines[0] + "\n",
            encoding="utf-8",
        )

        truncated_result = run(
            [
                "python",
                CHECKPOINT_VALIDATOR.name,
            ],
            cwd=temporary_root,
        )

        if truncated_result.returncode == 0:
            print(
                "FAIL: truncated ledger unexpectedly passed."
            )
            return 1

        truncated_output = (
            truncated_result.stdout
            + truncated_result.stderr
        )

        if "Ledger truncation detected" not in truncated_output:
            print(
                "FAIL: truncation was rejected without "
                "the expected diagnostic."
            )
            print(truncated_output)
            return 1

        ledger_path.write_text(
            original_ledger,
            encoding="utf-8",
        )

        entries = [
            json.loads(line)
            for line in original_ledger.splitlines()
            if line.strip()
        ]

        entries[0]["release"] = "rollback-replacement"

        ledger_path.write_text(
            "\n".join(
                json.dumps(
                    entry,
                    sort_keys=True,
                    separators=(",", ":"),
                )
                for entry in entries
            )
            + "\n",
            encoding="utf-8",
        )

        rollback_result = run(
            [
                "python",
                CHECKPOINT_VALIDATOR.name,
            ],
            cwd=temporary_root,
        )

        if rollback_result.returncode == 0:
            print(
                "FAIL: divergent ledger unexpectedly passed."
            )
            return 1

        rollback_output = (
            rollback_result.stdout
            + rollback_result.stderr
        )

        expected_messages = [
            "event_hash mismatch",
            "previous_hash mismatch",
            "head hash differs",
            "history diverges",
        ]

        if not any(
            message in rollback_output
            for message in expected_messages
        ):
            print(
                "FAIL: rollback/replacement was rejected "
                "without the expected diagnostic."
            )
            print(rollback_output)
            return 1

        canonical_checkpoint_directory = (
            ROOT
            / "nimble/governance/audit/checkpoints"
        )

        canonical_contents = sorted(
            path.name
            for path in canonical_checkpoint_directory.glob(
                "checkpoint-*.json"
            )
        )

        temporary_contents = sorted(
            path.name
            for path in checkpoint_directory.glob(
                "checkpoint-*.json"
            )
        )

        if (
            temporary_contents
            and temporary_contents == canonical_contents
        ):
            print(
                "FAIL: temporary checkpoint chain was not isolated."
            )
            return 1

        print("=" * 72)
        print("NIMBLE™ AUDIT CHECKPOINT TAMPER TEST")
        print("=" * 72)
        print("Valid checkpoint chain: PASS")
        print("Ledger truncation: DETECTED")
        print("Ledger rollback/replacement: DETECTED")
        print("Canonical checkpoint isolation: PASS")
        print("Status: PASS")

        return 0


if __name__ == "__main__":
    raise SystemExit(main())
