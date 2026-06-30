from __future__ import annotations
from typing import Any, Dict
from aletheus.plugins.runtime_plugin import RuntimePlugin
class RuntimePluginManager:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime; self.plugins: Dict[str, RuntimePlugin] = {}
    def register(self, plugin: RuntimePlugin) -> None:
        plugin.initialize(self.runtime); self.plugins[plugin.name] = plugin
    def list(self) -> Dict[str, Dict[str, str]]: return {name: {'version': plugin.version, 'description': plugin.description} for name, plugin in self.plugins.items()}
