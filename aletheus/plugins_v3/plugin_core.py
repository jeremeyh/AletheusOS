from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict
import uuid


def utc_now():
    return utc_now_iso()


@dataclass
class Plugin:

    plugin_id: str
    name: str
    version: str

    author: str = "6th Dimension Multimedia"
    description: str = ""

    enabled: bool = True
    installed_at: str = utc_now()
    updated_at: str = utc_now()


class AletheusPluginManager:

    VERSION = "3.1.0"

    def __init__(self):

        self.plugins: Dict[str, Plugin] = {}

    @property
    def version(self):
        return self.VERSION

    # ------------------------------------------------

    def bootstrap(self):

        if len(self.plugins) == 0:

            self.install(
                name="Card Hawk Foundation",
                version="3.1.0",
            )

        return self.statistics()

    # ------------------------------------------------

    def install(self, **payload):

        plugin = Plugin(
            plugin_id=str(uuid.uuid4()),
            name=payload.get("name", "Plugin"),
            version=payload.get("version", "1.0.0"),
            description=payload.get("description", ""),
        )

        self.plugins[plugin.plugin_id] = plugin

        return asdict(plugin)

    # ------------------------------------------------

    def enable(self, plugin_id):

        self.plugins[plugin_id].enabled = True
        self.plugins[plugin_id].updated_at = utc_now()

        return asdict(self.plugins[plugin_id])

    # ------------------------------------------------

    def disable(self, plugin_id):

        self.plugins[plugin_id].enabled = False
        self.plugins[plugin_id].updated_at = utc_now()

        return asdict(self.plugins[plugin_id])

    # ------------------------------------------------

    def update(self, plugin_id, version):

        plugin = self.plugins[plugin_id]

        if version:
            plugin.version = version

        plugin.updated_at = utc_now()

        return asdict(plugin)

    # ------------------------------------------------

    def remove(self, plugin_id):

        return asdict(self.plugins.pop(plugin_id))

    # ------------------------------------------------

    def list(self):

        return [
            asdict(plugin)
            for plugin in self.plugins.values()
        ]

    # ------------------------------------------------

    def status(self):

        return {
            "plugins": self.list()
        }

    # ------------------------------------------------

    def statistics(self):

        return {

            "version": self.VERSION,

            "plugins": len(self.plugins),

            "enabled": sum(
                p.enabled
                for p in self.plugins.values()
            ),

            "disabled": sum(
                not p.enabled
                for p in self.plugins.values()
            ),
        }


plugin_core = AletheusPluginManager()
