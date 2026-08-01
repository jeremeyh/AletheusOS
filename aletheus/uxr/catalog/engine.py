from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentDefinition:
    name: str
    required_props: tuple[str, ...] = ()
    fallback_rank: int = 100


class Engine:
    DEFAULT = (
        ComponentDefinition("LayoutContainer"),
        ComponentDefinition("Grid"),
        ComponentDefinition("MetricsCard", ("title", "value")),
        ComponentDefinition("DataGrid", ("columns", "rows")),
        ComponentDefinition("StatusBadge", ("status",)),
        ComponentDefinition("Timeline", ("events",)),
        ComponentDefinition("InteractiveChart", ("series",)),
        ComponentDefinition("ActionButtonGroup", ("buttons",)),
        ComponentDefinition("BannerAlert", ("message",)),
    )

    def __init__(self):
        self._items = {x.name: x for x in self.DEFAULT}

    def register(self, x):
        self._items[x.name] = x

    def names(self):
        return set(self._items)

    def get(self, name):
        return self._items[name]

    def fallback(self, preferred):
        return next((x for x in preferred if x in self._items), "BannerAlert")
