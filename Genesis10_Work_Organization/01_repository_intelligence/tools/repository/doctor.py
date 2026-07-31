#!/usr/bin/env python3
"""AletheusOS repository hygiene and structure diagnostics."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

IGNORED = {".git", ".venv", "__pycache__", ".pytest_cache", "archive", "history"}


def scan(root: Path) -> dict:
    top_files = [p for p in root.iterdir() if p.is_file()]
    top_dirs = [p for p in root.iterdir() if p.is_dir()]
    files = [
        p
        for p in root.rglob("*")
        if p.is_file() and not any(x in IGNORED for x in p.parts)
    ]
    suffixes = Counter(p.suffix or "[none]" for p in top_files)
    generated = [
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.name in {"__pycache__", ".pytest_cache", ".DS_Store"} or p.suffix == ".pyc"
    ]
    root_scripts = [p.name for p in top_files if p.suffix in {".py", ".sh"}]
    return {
        "root": str(root),
        "top_level_entries": len(top_files) + len(top_dirs),
        "top_level_files": len(top_files),
        "top_level_directories": len(top_dirs),
        "source_files_excluding_history_archive": len(files),
        "top_level_file_types": dict(sorted(suffixes.items())),
        "root_executable_scripts": len(root_scripts),
        "generated_artifacts_found": generated,
        "status": "clean" if not generated and len(root_scripts) < 200 else "attention",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2]
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = scan(args.root.resolve())
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("AletheusOS Repository Doctor")
        print(f"Status: {report['status'].upper()}")
        print(f"Top-level entries: {report['top_level_entries']}")
        print(f"Root executable scripts: {report['root_executable_scripts']}")
        print(f"Generated artifacts: {len(report['generated_artifacts_found'])}")
    return 0 if report["status"] == "clean" else 1


if __name__ == "__main__":
    raise SystemExit(main())
