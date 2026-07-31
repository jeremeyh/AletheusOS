from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import time
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
REPORT_DIRECTORY = ROOT / "reports" / "nimble"
LATEST_JSON = REPORT_DIRECTORY / "production-gate-latest.json"
LATEST_MARKDOWN = REPORT_DIRECTORY / "production-gate-latest.md"
HISTORY_JSONL = REPORT_DIRECTORY / "production-gate-history.jsonl"
LOG_FILE = REPORT_DIRECTORY / "production-gate-latest.log"

ASSET_DIRECTORY = ROOT / "nimble" / "apps" / "platform-shell" / "dist" / "assets"

PRIMARY_BUNDLE_LIMIT_BYTES = 500_000


def run(
    command: list[str],
    *,
    cwd: Path = ROOT,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
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
            stdout=(f"Command unavailable: {command[0]} ({error})"),
            stderr=None,
        )


def command_output(
    command: list[str],
    fallback: str = "unknown",
) -> str:
    result = run(command)

    if result.returncode != 0:
        return fallback

    value = result.stdout.strip()
    return value or fallback


def collect_git_metadata() -> dict[str, Any]:
    return {
        "commit": command_output(
            ["git", "rev-parse", "HEAD"],
        ),
        "short_commit": command_output(
            ["git", "rev-parse", "--short", "HEAD"],
        ),
        "branch": command_output(
            ["git", "branch", "--show-current"],
        ),
        "dirty": bool(
            command_output(
                ["git", "status", "--porcelain"],
                fallback="",
            )
        ),
        "tags_at_head": [
            line
            for line in command_output(
                ["git", "tag", "--points-at", "HEAD"],
                fallback="",
            ).splitlines()
            if line
        ],
    }


def shell_command_output(
    command: str,
    fallback: str = "unknown",
) -> str:
    result = run(
        [
            "/bin/bash",
            "-lc",
            command,
        ]
    )

    if result.returncode != 0:
        return fallback

    value = result.stdout.strip()
    return value or fallback


def collect_runtime_metadata() -> dict[str, str]:
    node_command = (
        'export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"; '
        '[ -s "$NVM_DIR/nvm.sh" ] '
        '&& . "$NVM_DIR/nvm.sh"; '
        "node --version"
    )

    npm_command = (
        'export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"; '
        '[ -s "$NVM_DIR/nvm.sh" ] '
        '&& . "$NVM_DIR/nvm.sh"; '
        "npm --version"
    )

    return {
        "python": platform.python_version(),
        "python_executable": sys.executable,
        "node": shell_command_output(
            node_command,
        ),
        "npm": shell_command_output(
            npm_command,
        ),
        "platform": platform.platform(),
    }


def collect_bundle_metadata() -> dict[str, Any]:
    chunks: list[dict[str, Any]] = []

    if ASSET_DIRECTORY.exists():
        for path in sorted(
            ASSET_DIRECTORY.glob("*.js"),
        ):
            chunks.append(
                {
                    "name": path.name,
                    "path": str(path.relative_to(ROOT)),
                    "bytes": path.stat().st_size,
                    "kind": (
                        "primary" if path.name.startswith("index-") else "secondary"
                    ),
                }
            )

    primary_candidates = [chunk for chunk in chunks if chunk["kind"] == "primary"]

    primary = (
        max(
            primary_candidates,
            key=lambda chunk: chunk["bytes"],
        )
        if primary_candidates
        else None
    )

    return {
        "primary_limit_bytes": PRIMARY_BUNDLE_LIMIT_BYTES,
        "primary": primary,
        "primary_within_budget": (
            primary is not None and primary["bytes"] <= PRIMARY_BUNDLE_LIMIT_BYTES
        ),
        "secondary_chunk_count": len(
            [chunk for chunk in chunks if chunk["kind"] == "secondary"]
        ),
        "chunks": chunks,
    }


def write_markdown(
    report: dict[str, Any],
) -> None:
    gate = report["gate"]
    bundle = report["bundle"]
    git = report["git"]
    runtime = report["runtime"]

    lines = [
        "# Nimble Production Gate Evidence",
        "",
        f"Generated: `{report['generated_at']}`",
        "",
        "## Result",
        "",
        f"- Status: **{gate['status']}**",
        f"- Exit code: `{gate['exit_code']}`",
        f"- Duration: `{gate['duration_seconds']:.2f}s`",
        f"- Commit: `{git['short_commit']}`",
        f"- Branch: `{git['branch']}`",
        f"- Working tree dirty: `{git['dirty']}`",
        "",
        "## Runtime",
        "",
        f"- Python: `{runtime['python']}`",
        f"- Node: `{runtime['node']}`",
        f"- npm: `{runtime['npm']}`",
        f"- Platform: `{runtime['platform']}`",
        "",
        "## Bundle",
        "",
    ]

    primary = bundle["primary"]

    if primary:
        lines.extend(
            [
                f"- Primary: `{primary['name']}`",
                f"- Primary bytes: `{primary['bytes']:,}`",
                (f"- Primary budget: `{bundle['primary_limit_bytes']:,}`"),
                (f"- Within budget: **{bundle['primary_within_budget']}**"),
            ]
        )
    else:
        lines.append("- Primary bundle: **not found**")

    lines.extend(
        [
            (f"- Secondary chunks: `{bundle['secondary_chunk_count']}`"),
            "",
            "### JavaScript chunks",
            "",
            "| Chunk | Kind | Bytes |",
            "|---|---:|---:|",
        ]
    )

    for chunk in bundle["chunks"]:
        lines.append(f"| `{chunk['name']}` | {chunk['kind']} | {chunk['bytes']:,} |")

    lines.extend(
        [
            "",
            "## Gate output",
            "",
            "```text",
            gate["output"].rstrip(),
            "```",
            "",
        ]
    )

    LATEST_MARKDOWN.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> int:
    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    started_at = datetime.now(
        UTC,
    )
    started = time.perf_counter()

    completed = run(
        ["./validate_nimble_production.sh"],
    )

    duration = time.perf_counter() - started

    LOG_FILE.write_text(
        completed.stdout,
        encoding="utf-8",
    )

    report: dict[str, Any] = {
        "schema_version": "1.0",
        "generated_at": started_at.isoformat(),
        "gate": {
            "status": ("PASS" if completed.returncode == 0 else "FAIL"),
            "exit_code": completed.returncode,
            "duration_seconds": round(
                duration,
                4,
            ),
            "output": completed.stdout,
        },
        "git": collect_git_metadata(),
        "runtime": collect_runtime_metadata(),
        "bundle": collect_bundle_metadata(),
        "environment": {
            "ci": os.environ.get("CI"),
            "github_actions": os.environ.get("GITHUB_ACTIONS"),
            "github_run_id": os.environ.get("GITHUB_RUN_ID"),
        },
    }

    serialized = json.dumps(
        report,
        indent=2,
        sort_keys=True,
    )

    LATEST_JSON.write_text(
        serialized + "\n",
        encoding="utf-8",
    )

    with HISTORY_JSONL.open(
        "a",
        encoding="utf-8",
    ) as handle:
        history_record = {
            **report,
            "gate": {
                key: value for key, value in report["gate"].items() if key != "output"
            },
        }

        handle.write(
            json.dumps(
                history_record,
                sort_keys=True,
            )
            + "\n"
        )

    write_markdown(report)

    print(completed.stdout, end="")
    print()
    print("=" * 72)
    print("NIMBLE™ PRODUCTION EVIDENCE")
    print("=" * 72)
    print(
        "JSON:",
        LATEST_JSON.relative_to(ROOT),
    )
    print(
        "Markdown:",
        LATEST_MARKDOWN.relative_to(ROOT),
    )
    print(
        "Log:",
        LOG_FILE.relative_to(ROOT),
    )
    print(
        "History:",
        HISTORY_JSONL.relative_to(ROOT),
    )
    print(
        "Status:",
        report["gate"]["status"],
    )

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
