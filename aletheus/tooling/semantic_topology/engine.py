from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT_HINTS = {
    "constitutional_root": ("constitution", "principle", "breadth", "council"),
    "runtime_root": ("runtime", "crk", "registry", "mission"),
    "intelligence_root": ("evidence", "knowledge", "reason", "memory", "predictive"),
    "security_root": ("spartan", "sentinel", "span", "watch", "conclave", "security"),
    "product_root": ("card hawk", "thor", "a•3ye", "a3ye"),
}


def classify(name: str) -> str:
    lowered = name.casefold()
    for label, hints in ROOT_HINTS.items():
        if any(hint in lowered for hint in hints):
            return label
    return "supporting_root"


class Engine:
    def __init__(self, paths: Path, catalog: Path, output: Path) -> None:
        self.paths = paths
        self.catalog = catalog
        self.output = output

    def build(self) -> dict[str, Any]:
        paths = json.loads(self.paths.read_text(encoding="utf-8"))
        catalog = json.loads(self.catalog.read_text(encoding="utf-8"))
        categories = {
            str(item.get("name")): str(item.get("category", "unknown"))
            for item in catalog.get("entries", [])
            if isinstance(item, dict)
        }

        classified = [
            {
                "node": root,
                "semantic_class": classify(root),
                "catalog_category": categories.get(root, "unknown"),
                "intentional_root": classify(root) != "supporting_root",
            }
            for root in paths.get("roots", [])
        ]
        counts = Counter(item["semantic_class"] for item in classified)
        report = {
            "roots": classified,
            "root_count": len(classified),
            "class_counts": dict(sorted(counts.items())),
            "ambiguous_roots": [
                item["node"]
                for item in classified
                if item["semantic_class"] == "supporting_root"
            ],
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "semantic-root-classification.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
