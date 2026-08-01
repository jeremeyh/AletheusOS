from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DOMAIN_RULES = {
    "constitutional": ("principle", "constitution", "council", "truth", "virtue"),
    "runtime": (
        "runtime",
        "registry",
        "mission",
        "execution",
        "scheduler",
        "capability",
    ),
    "intelligence": (
        "engine",
        "evidence",
        "knowledge",
        "reason",
        "memory",
        "predictive",
        "planning",
        "decision",
    ),
    "security": (
        "spartan",
        "sentinel",
        "span",
        "watch",
        "conclave",
        "security",
        "threat",
        "audit",
        "risk",
    ),
    "perception": (
        "vision",
        "ocr",
        "recognition",
        "verification",
        "inspection",
        "document",
        "a•3ye",
        "a3ye",
    ),
    "product": ("card hawk", "thor", "q-def", "d-def", "strike", "nuclear", "asset"),
    "infrastructure": ("fabric", "mesh", "ledger", "vault", "trust", "identity"),
}


def resolve_domain(name: str, category: str) -> tuple[str, str]:
    text = f"{name} {category}".casefold()
    for domain, hints in DOMAIN_RULES.items():
        if any(hint in text for hint in hints):
            return domain, "rule_match"
    return "platform_support", "intentional_root_declaration"


class Engine:
    def __init__(self, semantic_roots: Path, catalog: Path, output: Path) -> None:
        self.semantic_roots = semantic_roots
        self.catalog = catalog
        self.output = output

    def build(self) -> dict[str, Any]:
        roots = json.loads(self.semantic_roots.read_text(encoding="utf-8"))
        catalog = json.loads(self.catalog.read_text(encoding="utf-8"))
        categories = {
            str(item.get("name")): str(item.get("category", "unknown"))
            for item in catalog.get("entries", [])
            if isinstance(item, dict)
        }
        resolved = []
        for item in roots.get("roots", []):
            if not isinstance(item, dict):
                continue
            name = str(item.get("node"))
            domain, basis = resolve_domain(name, categories.get(name, "unknown"))
            resolved.append(
                {
                    "root": name,
                    "parent_domain": domain,
                    "resolution_basis": basis,
                    "intentional_root": basis == "intentional_root_declaration",
                    "status": "resolved",
                }
            )
        report = {
            "resolved_roots": resolved,
            "resolved_count": len(resolved),
            "unresolved_roots": [],
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "explicit-root-domain-resolution.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
