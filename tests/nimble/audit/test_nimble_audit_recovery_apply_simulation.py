#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

SCRIPTS = [
    "bin/append_nimble_audit_event.py",
    "bin/create_nimble_audit_checkpoint.py",
    "bin/create_nimble_signed_audit_anchor.py",
    "bin/create_nimble_audit_recovery_source.py",
    "bin/validate_nimble_audit_ledger.py",
    "bin/validate_nimble_audit_checkpoints.py",
    "bin/validate_nimble_signed_audit_anchor.py",
    "bin/validate_nimble_audit_recovery_source.py",
    "bin/plan_nimble_audit_recovery.py",
    "bin/apply_nimble_audit_recovery.py",
]

LEDGER_RELATIVE = Path(
    "nimble/governance/audit/"
    "deployment-audit-ledger.jsonl"
)

SNAPSHOT_RELATIVE = Path(
    "reports/nimble/recovery/snapshots"
)


def run(
    command: list[str],
    *,
    cwd: Path,
    expected: int | None = 0,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        timeout=90,
        env={
            **os.environ,
            "GIT_TERMINAL_PROMPT": "0",
            "GIT_EDITOR": "true",
            "GIT_SEQUENCE_EDITOR": "true",
            "PYTHONUNBUFFERED": "1",
        },
    )

    if expected is not None and result.returncode != expected:
        raise RuntimeError(
            "Command failed:\n"
            + " ".join(command)
            + "\n\nSTDOUT:\n"
            + result.stdout
            + "\nSTDERR:\n"
            + result.stderr
        )

    return result


def sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def initialize_git(root: Path) -> None:
    commands = [
        ["git", "init"],
        [
            "git",
            "config",
            "user.name",
            "Nimble Recovery Test",
        ],
        [
            "git",
            "config",
            "user.email",
            "nimble-recovery@example.invalid",
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
            "Initialize recovery simulation",
        ],
    ]

    for command in commands:
        run(command, cwd=root)


def copy_runtime(root: Path) -> None:
    shutil.copytree(
        ROOT / "nimble",
        root / "nimble",
    )

    reports_source = ROOT / "reports/nimble"

    if reports_source.exists():
        shutil.copytree(
            reports_source,
            root / "reports/nimble",
        )
    else:
        (
            root / "reports/nimble"
        ).mkdir(parents=True)

    (root / "bin").mkdir(parents=True, exist_ok=True)

    for script in SCRIPTS:
        shutil.copy2(
            ROOT / script,
            root / script,
        )

    ledger = root / LEDGER_RELATIVE

    ledger.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    ledger.write_text(
        "",
        encoding="utf-8",
    )

    checkpoints = (
        root
        / "nimble/governance/audit/checkpoints"
    )

    if checkpoints.exists():
        shutil.rmtree(checkpoints)

    checkpoints.mkdir(
        parents=True,
        exist_ok=True,
    )

    recovery_reports = (
        root
        / "reports/nimble/recovery"
    )

    if recovery_reports.exists():
        shutil.rmtree(recovery_reports)

    recovery_reports.mkdir(
        parents=True,
        exist_ok=True,
    )

    initialize_git(root)


def append_event(
    root: Path,
    event_type: str,
) -> None:
    run(
        [
            "python",
            "bin/append_nimble_audit_event.py",
            "--event-type",
            event_type,
            "--environment",
            "staging",
            "--release",
            "recovery-apply-simulation-v0.1",
            "--revision",
            "simulation-revision",
            "--metadata-json",
            '{"simulation":true}',
        ],
        cwd=root,
    )


def prepare_recoverable_state(
    root: Path,
) -> tuple[bytes, bytes]:
    ledger = root / LEDGER_RELATIVE

    append_event(
        root,
        "deployment_started",
    )

    append_event(
        root,
        "deployment_completed",
    )

    run(
        [
            "python",
            "bin/create_nimble_audit_checkpoint.py",
            "--release",
            "recovery-apply-simulation-v0.1",
        ],
        cwd=root,
    )

    run(
        [
            "python",
            "bin/create_nimble_signed_audit_anchor.py",
        ],
        cwd=root,
    )

    run(
        [
            "python",
            "bin/create_nimble_audit_recovery_source.py",
        ],
        cwd=root,
    )

    trusted_bytes = ledger.read_bytes()

    lines = [
        line
        for line in trusted_bytes.decode(
            "utf-8"
        ).splitlines()
        if line.strip()
    ]

    if len(lines) < 2:
        raise RuntimeError(
            "Simulation requires at least two events."
        )

    truncated_bytes = (
        lines[0] + "\n"
    ).encode("utf-8")

    ledger.write_bytes(
        truncated_bytes
    )

    plan = run(
        [
            "python",
            "bin/plan_nimble_audit_recovery.py",
        ],
        cwd=root,
        expected=2,
    )

    if (
        "Classification: checkpoint_ahead_of_ledger"
        not in plan.stdout
    ):
        raise RuntimeError(
            "Planner did not classify the truncated "
            "ledger as checkpoint_ahead_of_ledger.\n"
            + plan.stdout
        )

    if (
        "Recommended action: restore_missing_suffix"
        not in plan.stdout
    ):
        raise RuntimeError(
            "Planner did not authorize suffix restoration."
        )

    return trusted_bytes, truncated_bytes


def verify_successful_apply() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        copy_runtime(root)

        trusted_bytes, truncated_bytes = (
            prepare_recoverable_state(root)
        )

        ledger = root / LEDGER_RELATIVE

        result = run(
            [
                "python",
                "bin/apply_nimble_audit_recovery.py",
                "--confirm",
                "APPLY-AUDIT-RECOVERY",
            ],
            cwd=root,
        )

        if "Atomic replacement: PASS" not in result.stdout:
            raise RuntimeError(
                "Atomic replacement was not confirmed."
            )

        if (
            "Recovery provenance event: APPENDED"
            not in result.stdout
        ):
            raise RuntimeError(
                "Recovery provenance was not appended."
            )

        snapshots = sorted(
            (
                root / SNAPSHOT_RELATIVE
            ).glob(
                "deployment-audit-ledger-*.jsonl"
            )
        )

        if len(snapshots) != 1:
            raise RuntimeError(
                "Exactly one pre-recovery snapshot "
                "was expected."
            )

        if snapshots[0].read_bytes() != truncated_bytes:
            raise RuntimeError(
                "Pre-recovery snapshot does not contain "
                "the truncated ledger."
            )

        restored_lines = [
            json.loads(line)
            for line in ledger.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        ]

        trusted_lines = [
            json.loads(line)
            for line in trusted_bytes.decode(
                "utf-8"
            ).splitlines()
            if line.strip()
        ]

        if restored_lines[:len(trusted_lines)] != trusted_lines:
            raise RuntimeError(
                "Recovered ledger prefix differs from "
                "the trusted source."
            )

        final_event = restored_lines[-1]

        if (
            final_event.get("event_type")
            != "audit_recovery_completed"
        ):
            raise RuntimeError(
                "Final ledger event is not recovery provenance."
            )

        run(
            [
                "python",
                "bin/validate_nimble_audit_ledger.py",
            ],
            cwd=root,
        )


def verify_validation_failure_rollback() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        copy_runtime(root)

        _, truncated_bytes = (
            prepare_recoverable_state(root)
        )

        ledger = root / LEDGER_RELATIVE

        validator = (
            root
            / "bin/validate_nimble_audit_ledger.py"
        )

        validator.write_text(
            "#!/usr/bin/env python3\n"
            "print('FAIL: injected post-recovery failure')\n"
            "raise SystemExit(1)\n",
            encoding="utf-8",
        )

        result = run(
            [
                "python",
                "bin/apply_nimble_audit_recovery.py",
                "--confirm",
                "APPLY-AUDIT-RECOVERY",
            ],
            cwd=root,
            expected=None,
        )

        if result.returncode == 0:
            raise RuntimeError(
                "Injected validation failure unexpectedly passed."
            )

        output = result.stdout + result.stderr

        if (
            "pre-recovery snapshot was restored"
            not in output
        ):
            raise RuntimeError(
                "Recovery failure did not report rollback."
            )

        if ledger.read_bytes() != truncated_bytes:
            raise RuntimeError(
                "Failed recovery did not restore the "
                "pre-recovery ledger."
            )

        snapshots = list(
            (
                root / SNAPSHOT_RELATIVE
            ).glob(
                "deployment-audit-ledger-*.jsonl"
            )
        )

        if not snapshots:
            raise RuntimeError(
                "Rollback scenario did not preserve a snapshot."
            )


def main() -> int:
    canonical_ledger = ROOT / LEDGER_RELATIVE
    canonical_before = sha256(canonical_ledger)

    verify_successful_apply()
    verify_validation_failure_rollback()

    canonical_after = sha256(canonical_ledger)

    if canonical_before != canonical_after:
        print(
            "FAIL: canonical deployment audit ledger changed."
        )
        return 1

    print("=" * 72)
    print("NIMBLE™ AUDIT RECOVERY APPLY SIMULATION")
    print("=" * 72)
    print("Recoverable truncation classification: PASS")
    print("Operator confirmation enforcement: PASS")
    print("Pre-recovery snapshot: PASS")
    print("Trusted source revalidation: PASS")
    print("Atomic ledger replacement: PASS")
    print("Post-recovery validation: PASS")
    print("Recovery provenance append: PASS")
    print("Validation-failure rollback: PASS")
    print("Canonical ledger isolation: PASS")
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
