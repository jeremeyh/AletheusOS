from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class RegistryEngine:
    def __init__(self, authority: Path, twin: Path, output: Path) -> None:
        self.authority = authority
        self.twin = twin
        self.output = output

    def build(self) -> dict[str, Any]:
        authority = json.loads(self.authority.read_text(encoding="utf-8"))
        twin = json.loads(self.twin.read_text(encoding="utf-8"))
        capabilities = authority.get("capabilities", [])
        nodes = twin.get("nodes", [])
        registry = {
            "generated_at": datetime.now(UTC).isoformat(),
            "capabilities": capabilities if isinstance(capabilities, list) else [],
            "entities": nodes if isinstance(nodes, list) else [],
            "module_assignments": authority.get("module_assignments", {}),
            "unresolved_modules": authority.get("unresolved_modules", []),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-registry.json").write_text(
            json.dumps(registry, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "authority-index.json").write_text(
            json.dumps(
                {
                    item.get("name"): item.get("runtime_role")
                    for item in registry["capabilities"]
                    if isinstance(item, dict)
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        (self.output / "engine-index.json").write_text(
            json.dumps(
                [
                    item
                    for item in registry["entities"]
                    if isinstance(item, dict)
                    and item.get("node_type") in {"engine", "runtime", "service"}
                ],
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        (self.output / "constitutional-registry.md").write_text(
            "# Constitutional Registry\n\n"
            f"- Capabilities: **{len(registry['capabilities'])}**\n"
            f"- Entities: **{len(registry['entities'])}**\n",
            encoding="utf-8",
        )
        return registry
