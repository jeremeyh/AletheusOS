from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[2]
RESTORE_ROOT = ROOT / ".aletheus_restore_points"

EXCLUDE_DIRS = {
    ".git", "venv", ".venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "node_modules",
    ".aletheus_restore_points",
}

EXCLUDE_PREFIXES = {
    "logs/",
    "runtime_state/snapshots/",
}

INCLUDE_SUFFIXES = {
    ".py", ".json", ".toml", ".yaml", ".yml", ".md", ".txt",
    ".csv", ".sql", ".html", ".css", ".js",
}


def run(cmd: list[str]) -> dict:
    proc = subprocess.run(
        cmd,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def should_include(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()

    if any(part in EXCLUDE_DIRS for part in path.parts):
        return False

    if any(rel.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
        return False

    if path.is_file() and path.suffix in INCLUDE_SUFFIXES:
        return True

    return False


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    restore_dir = RESTORE_ROOT / f"restore_{timestamp}"
    restore_dir.mkdir(parents=True, exist_ok=False)

    manifest = {
        "name": f"AletheusOS Restore Point {timestamp}",
        "created_at": datetime.now().isoformat(),
        "project_root": str(ROOT),
        "git_status": run(["git", "status", "--short"]),
        "git_head": run(["git", "rev-parse", "HEAD"]),
        "runtime_census": run([sys.executable, "tools/maintenance/runtime_census.py"]),
        "files": {},
    }

    source_zip = restore_dir / "source_snapshot.zip"

    with ZipFile(source_zip, "w", ZIP_DEFLATED) as archive:
        for path in ROOT.rglob("*"):
            if not should_include(path):
                continue

            rel = path.relative_to(ROOT).as_posix()
            manifest["files"][rel] = {
                "sha256": sha256(path),
                "size": path.stat().st_size,
            }
            archive.write(path, rel)

    manifest_path = restore_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    latest = RESTORE_ROOT / "LATEST.txt"
    latest.write_text(str(restore_dir), encoding="utf-8")

    print("AletheusOS Restore Point Created")
    print("=" * 40)
    print(f"Restore point: {restore_dir}")
    print(f"Snapshot:      {source_zip}")
    print(f"Manifest:      {manifest_path}")
    print(f"Files hashed:  {len(manifest['files'])}")
    print()
    print("Runtime census result:")
    print(f"Return code: {manifest['runtime_census']['returncode']}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
