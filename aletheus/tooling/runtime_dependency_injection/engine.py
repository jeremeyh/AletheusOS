from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .container import DependencyContainer


@dataclass(slots=True)
class RuntimeEngineProxy:
    name: str
    authority: str | None
    parent: str | None


class InjectionEngine:
    def __init__(self, registry: Path, authority_map: Path, output: Path) -> None:
        self.registry = registry
        self.authority_map = authority_map
        self.output = output

    def build(self) -> dict[str, Any]:
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        authority = json.loads(self.authority_map.read_text(encoding="utf-8"))
        authority_by_name = {
            str(item.get("name")): item
            for item in authority.get("capabilities", [])
            if isinstance(item, dict)
        }

        container = DependencyContainer()
        names = []
        for item in registry.get("engines", []):
            if not isinstance(item, dict):
                continue
            name = str(item.get("engine_name"))
            names.append(name)
            authority_entry = authority_by_name.get(name, {})
            container.register(
                name,
                lambda _container, n=name, a=authority_entry: RuntimeEngineProxy(
                    name=n,
                    authority=a.get("authority"),
                    parent=a.get("parent"),
                ),
            )

        resolved = []
        for name in sorted(names):
            proxy = container.resolve(name)
            resolved.append(
                {
                    "engine_name": proxy.name,
                    "authority": proxy.authority,
                    "parent": proxy.parent,
                    "injected": True,
                }
            )
        report = {"bindings": resolved, "binding_count": len(resolved)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-dependency-injection.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
