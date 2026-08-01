from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def normalize(name: str) -> str:
    return "".join(ch for ch in name.casefold() if ch.isalnum())


class EcosystemCatalogEngine:
    def __init__(self, base_catalog: Path, expansion: Path, output: Path) -> None:
        self.base_catalog = base_catalog
        self.expansion = expansion
        self.output = output

    def build(self) -> dict[str, Any]:
        base = json.loads(self.base_catalog.read_text(encoding="utf-8"))
        expansion = json.loads(self.expansion.read_text(encoding="utf-8"))
        base_entries = base.get("entries", [])
        extra_entries = expansion.get("entries", [])
        if not isinstance(base_entries, list) or not isinstance(extra_entries, list):
            raise TypeError("Catalog entries must be lists.")

        merged: dict[str, dict[str, Any]] = {}
        for item in [*base_entries, *extra_entries]:
            if not isinstance(item, dict):
                continue
            key = normalize(str(item.get("name", "")))
            if not key:
                continue
            if key in merged:
                combined = dict(merged[key])
                for field in (
                    "aliases",
                    "must_not_own",
                    "inputs",
                    "outputs",
                    "mesh_connections",
                ):
                    values = {
                        str(v)
                        for v in [
                            *combined.get(field, []),
                            *item.get(field, []),
                        ]
                    }
                    combined[field] = sorted(values)
                merged[key] = combined
            else:
                merged[key] = dict(item)

        catalog = {
            "schema_version": "2.0",
            "entries": sorted(merged.values(), key=lambda item: str(item.get("name"))),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "canonical-ecosystem-catalog.json").write_text(
            json.dumps(catalog, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        counts: dict[str, int] = {}
        for item in catalog["entries"]:
            category = str(item.get("category", "unknown"))
            counts[category] = counts.get(category, 0) + 1
        (self.output / "catalog-category-counts.json").write_text(
            json.dumps(counts, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return catalog
