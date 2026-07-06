from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESTORE_ROOT = ROOT / ".aletheus_restore_points"
LATEST = RESTORE_ROOT / "LATEST.txt"

EXCLUDE_DIRS = {
    ".git", "venv", ".venv", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "node_modules",
    ".aletheus_restore_points",
}

EXCLUDE_NAMES = {
    ".DS_Store",
}

EXCLUDE_SUFFIXES = {
    ".pyc", ".pyo", ".db", ".sqlite", ".sqlite3", ".log",
}

EXCLUDE_PATTERNS = (
    ".backup",
    ".backup_",
)

EXCLUDE_PREFIXES = (
    "logs/",
    "runtime_state/",
    "reports/runtime-health",
    "data/runtime_events",
)

INCLUDE_SUFFIXES = {
    ".py", ".json", ".toml", ".yaml", ".yml", ".md", ".txt",
    ".csv", ".sql", ".html", ".css", ".js",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def should_check(path: Path) -> bool:
    if not path.is_file():
        return False

    rel = path.relative_to(ROOT).as_posix()
    rel_parts = path.relative_to(ROOT).parts

    if any(part in EXCLUDE_DIRS for part in rel_parts):
        return False

    if path.name in EXCLUDE_NAMES:
        return False

    if path.suffix in EXCLUDE_SUFFIXES:
        return False

    if any(pattern in path.name for pattern in EXCLUDE_PATTERNS):
        return False

    if any(rel.startswith(prefix) for prefix in EXCLUDE_PREFIXES):
        return False

    if path.suffix not in INCLUDE_SUFFIXES:
        return False

    return True


def main():
    if not LATEST.exists():
        print("No restore point found. Run create_restore_point.py first.")
        raise SystemExit(1)

    restore_dir = Path(LATEST.read_text().strip())
    manifest_path = restore_dir / "manifest.json"

    if not manifest_path.exists():
        print(f"Missing manifest: {manifest_path}")
        raise SystemExit(1)

    manifest = json.loads(manifest_path.read_text())
    baseline_raw = manifest.get("files", {})

    baseline = {
        rel: meta
        for rel, meta in baseline_raw.items()
        if should_check(ROOT / rel)
    }

    current = {}

    for path in ROOT.rglob("*"):
        if not should_check(path):
            continue

        rel = path.relative_to(ROOT).as_posix()
        current[rel] = {
            "sha256": sha256(path),
            "size": path.stat().st_size,
        }

    baseline_files = set(baseline)
    current_files = set(current)

    added = sorted(current_files - baseline_files)
    deleted = sorted(baseline_files - current_files)

    changed = []
    for rel in sorted(baseline_files & current_files):
        if baseline[rel]["sha256"] != current[rel]["sha256"]:
            changed.append(rel)

    print("AletheusOS Drift Detection")
    print("=" * 40)
    print(f"Restore point: {restore_dir.name}")
    print(f"Baseline files: {len(baseline_files)}")
    print(f"Current files:  {len(current_files)}")
    print()

    print(f"Added:   {len(added)}")
    print(f"Changed: {len(changed)}")
    print(f"Deleted: {len(deleted)}")
    print()

    if added:
        print("Added files")
        print("-" * 40)
        for item in added[:50]:
            print(f"+ {item}")
        if len(added) > 50:
            print(f"... {len(added) - 50} more")
        print()

    if changed:
        print("Changed files")
        print("-" * 40)
        for item in changed[:50]:
            print(f"~ {item}")
        if len(changed) > 50:
            print(f"... {len(changed) - 50} more")
        print()

    if deleted:
        print("Deleted files")
        print("-" * 40)
        for item in deleted[:50]:
            print(f"- {item}")
        if len(deleted) > 50:
            print(f"... {len(deleted) - 50} more")
        print()

    if added or changed or deleted:
        print("OVERALL: DRIFT DETECTED")
        raise SystemExit(1)

    print("OVERALL: NO DRIFT")


if __name__ == "__main__":
    main()
