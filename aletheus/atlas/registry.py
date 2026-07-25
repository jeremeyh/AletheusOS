from __future__ import annotations

from .models import ArchitectureGraph


class AtlasRegistry:
    """Stores the latest ArchitectureGraph in memory."""

    def __init__(self) -> None:
        self._graph: ArchitectureGraph | None = None

    def publish(self, graph: ArchitectureGraph) -> None:
        self._graph = graph

    def current(self) -> ArchitectureGraph | None:
        return self._graph
