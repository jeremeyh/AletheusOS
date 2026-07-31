from __future__ import annotations

import hashlib
import json
import platform
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

DIST = ROOT / "nimble" / "apps" / "platform-shell" / "dist"

CONTRACT = ROOT / "nimble" / "governance" / "deployment" / "deployment-contract.json"

OUTPUT = ROOT / "nimble" / "governance" / "deployment" / "build-metadata.json"

REPORT = ROOT / "reports" / "nimble" / "build-metadata-latest.md"


def command_output(
    command: list[str],
) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return completed.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(block)

    return digest.hexdigest()


def collect_artifacts() -> list[dict[str, Any]]:
    if not DIST.exists():
        raise FileNotFoundError(
            "Frontend distribution is missing. Run the Nimble production build first."
        )

    artifacts: list[dict[str, Any]] = []

    for path in sorted(DIST.rglob("*")):
        if not path.is_file():
            continue

        artifacts.append(
            {
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )

    return artifacts


def main() -> int:
    if not CONTRACT.exists():
        print("FAIL: Deployment contract is missing.")
        return 1

    artifacts = collect_artifacts()

    metadata = {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "source": {
            "commit": command_output(["git", "rev-parse", "HEAD"]),
            "short_commit": command_output(["git", "rev-parse", "--short", "HEAD"]),
            "branch": command_output(["git", "branch", "--show-current"]),
        },
        "runtime": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "node": command_output(["node", "--version"]),
            "npm": command_output(["npm", "--version"]),
        },
        "deployment_contract": {
            "path": str(CONTRACT.relative_to(ROOT)),
            "sha256": sha256_file(CONTRACT),
        },
        "frontend": {
            "distribution": str(DIST.relative_to(ROOT)),
            "file_count": len(artifacts),
            "total_bytes": sum(item["bytes"] for item in artifacts),
            "artifacts": artifacts,
        },
    }

    OUTPUT.write_text(
        json.dumps(
            metadata,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    REPORT.write_text(
        "\n".join(
            [
                "# Nimble Build Metadata",
                "",
                f"Generated: `{metadata['generated_at']}`",
                (f"Commit: `{metadata['source']['commit']}`"),
                (f"Branch: `{metadata['source']['branch']}`"),
                "",
                "## Runtime",
                "",
                (f"- Python: `{metadata['runtime']['python']}`"),
                (f"- Node: `{metadata['runtime']['node']}`"),
                (f"- npm: `{metadata['runtime']['npm']}`"),
                "",
                "## Frontend distribution",
                "",
                (f"- Files: `{metadata['frontend']['file_count']}`"),
                (f"- Total bytes: `{metadata['frontend']['total_bytes']}`"),
                (
                    "- Deployment contract SHA-256: "
                    f"`{metadata['deployment_contract']['sha256']}`"
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ BUILD METADATA")
    print("=" * 72)
    print(
        "Commit:",
        metadata["source"]["short_commit"],
    )
    print(
        "Frontend files:",
        metadata["frontend"]["file_count"],
    )
    print(
        "Frontend bytes:",
        metadata["frontend"]["total_bytes"],
    )
    print(
        "Metadata:",
        OUTPUT.relative_to(ROOT),
    )
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
