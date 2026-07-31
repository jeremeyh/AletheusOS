"""Directed module-import graph."""

from __future__ import annotations

from collections import defaultdict

from .models import ModuleRecord


class RepositoryGraph:
    def __init__(self, modules: list[ModuleRecord]) -> None:
        self.modules = {module.module: module for module in modules}
        self.outgoing: dict[str, set[str]] = defaultdict(set)
        self.incoming: dict[str, set[str]] = defaultdict(set)
        self._build()

    def _build(self) -> None:
        known = set(self.modules)
        for module in self.modules.values():
            for imported in module.imports:
                target = self._resolve_import(imported, known)
                if target is None or target == module.module:
                    continue
                self.outgoing[module.module].add(target)
                self.incoming[target].add(module.module)

    @staticmethod
    def _resolve_import(imported: str, known: set[str]) -> str | None:
        candidate = imported
        while candidate:
            if candidate in known:
                return candidate
            candidate = candidate.rpartition(".")[0]
        return None

    def fan_in(self, module: str) -> int:
        return len(self.incoming.get(module, set()))

    def fan_out(self, module: str) -> int:
        return len(self.outgoing.get(module, set()))
