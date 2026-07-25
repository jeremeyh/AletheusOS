from __future__ import annotations

from typing import Any

from services.context import PipelineContext
from services.plugin_loader import PluginLoader


class Pipeline:
    def __init__(self, plugin_loader: PluginLoader) -> None:
        self.plugin_loader = plugin_loader

    def run(self, command: str = "runtime.pipeline", payload: dict[str, Any] | None = None) -> PipelineContext:
        context = PipelineContext(command=command, payload=payload or {})
        for plugin in self.plugin_loader.enabled_plugins():
            try:
                context = plugin.execute(context)
            except Exception as exc:
                context.add_error(f"{plugin.name} failed: {exc}")
        return context
