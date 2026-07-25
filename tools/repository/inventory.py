#!/usr/bin/env python3
"""Repository inventory discovery."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
}


@dataclass(frozen=True, slots=True)
class InventoryEntry:
    path: Path
    relative_path: Path
    size: int
    suffix: str
    executable: bool
    sha256: str | None

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["path"] = str(self.path)
        result["relative_path"] = str(self.relative_path)
        return result


class RepositoryInventory:
    def __init__(
        self,
        root: Path | str = ".",
        excluded_directories: Iterable[str] = DEFAULT_EXCLUDED_DIRECTORIES,
    ) -> None:
        self.root = Path(root).resolve()
        self.excluded_directories = set(excluded_directories)

    def iter_files(self, include_hashes: bool = False) -> Iterator[InventoryEntry]:
        for path in sorted(self.root.rglob("*")):
            if not path.is_file():
                continue

            relative = path.relative_to(self.root)

            if any(part in self.excluded_directories for part in relative.parts):
                continue

            stat = path.stat()

            yield InventoryEntry(
                path=path,
                relative_path=relative,
                size=stat.st_size,
                suffix=path.suffix.lower(),
                executable=bool(stat.st_mode & 0o111),
                sha256=self._sha256(path) if include_hashes else None,
            )

    def collect(self, include_hashes: bool = False) -> list[InventoryEntry]:
        return list(self.iter_files(include_hashes=include_hashes))

    def root_files(self) -> list[InventoryEntry]:
        return [
            entry
            for entry in self.iter_files()
            if len(entry.relative_path.parts) == 1
        ]

    def write_json(
        self,
        output: Path | str,
        include_hashes: bool = False,
    ) -> Path:
        destination = Path(output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        entries = self.collect(include_hashes=include_hashes)

        payload = {
            "root": str(self.root),
            "count": len(entries),
            "entries": [entry.to_dict() for entry in entries],
        }

        destination.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8",
        )
        return destination

    @staticmethod
    def _sha256(path: Path) -> str:
        digest = hashlib.sha256()

        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)

        return digest.hexdigest()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Inventory repository files.")
    parser.add_argument("--root", default=".")
    parser.add_argument("--output")
    parser.add_argument("--hashes", action="store_true")
    args = parser.parse_args()

    inventory = RepositoryInventory(args.root)
    entries = inventory.collect(include_hashes=args.hashes)

    if args.output:
        output = inventory.write_json(args.output, include_hashes=args.hashes)
        print(f"Wrote {len(entries)} entries to {output}")
    else:
        for entry in entries:
            print(entry.relative_path)
        print(f"\nFiles: {len(entries)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
