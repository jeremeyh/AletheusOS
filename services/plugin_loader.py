from __future__ import annotations

import importlib

from plugins.base_plugin import BasePlugin

DEFAULT_PLUGIN_MODULES = [
    "plugins.perch",
    "plugins.talon",
    "plugins.strike",
    "plugins.soar",
    "plugins.roost",
]


class PluginLoader:
    def __init__(self) -> None:
        self.plugins: dict[str, BasePlugin] = {}

    def load_defaults(self) -> dict[str, BasePlugin]:
        for module_name in DEFAULT_PLUGIN_MODULES:
            self.load(module_name)
        return self.plugins

    def load(self, module_name: str) -> BasePlugin:
        module = importlib.import_module(module_name)
        plugin = module.Plugin()
        self.plugins[plugin.name] = plugin
        return plugin

    def manifests(self) -> list[dict]:
        return [plugin.manifest() for plugin in self.plugins.values()]

    def enabled_plugins(self) -> list[BasePlugin]:
        return [plugin for plugin in self.plugins.values() if plugin.enabled]
