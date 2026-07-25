from __future__ import annotations

from typing import Any

from aletheus.plugins.runtime_plugin import RuntimePlugin


class RuntimePluginManager:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime; self.plugins: dict[str, RuntimePlugin] = {}
    def register(self, plugin: RuntimePlugin) -> None:
        plugin.initialize(self.runtime); self.plugins[plugin.name] = plugin
    def list(self) -> dict[str, dict[str, str]]: return {name: {'version': plugin.version, 'description': plugin.description} for name, plugin in self.plugins.items()}
