from dataclasses import dataclass, field
import uuid

@dataclass
class PluginDefinition:
    name: str
    category: str
    description: str = ""
    enabled: bool = True
    plugin_id: str = field(default_factory=lambda: f"PLUG-{uuid.uuid4().hex[:10].upper()}")

class PluginRegistry:
    """7.0F — Plugin & Extension Framework™."""

    _plugins = {}

    @classmethod
    def register(cls, name, category, description="", enabled=True):
        plugin = PluginDefinition(name, category, description, enabled)
        cls._plugins[name] = plugin
        return plugin

    @classmethod
    def all(cls):
        return list(cls._plugins.values())

    @classmethod
    def seed_defaults(cls):
        if not cls._plugins:
            cls.register("eBay Provider", "Marketplace", "Marketplace provider plugin.")
            cls.register("PSA Population", "Grading", "Population and grade distribution plugin.")
            cls.register("Portfolio Heatmap", "Analytics", "Custom dashboard extension.")
        return cls.all()
