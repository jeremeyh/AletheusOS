from __future__ import annotations

from typing import Optional

from .models import ArchitectureGraph


class AtlasRegistry:
    """Stores the latest ArchitectureGraph in memory."""

    def __init__(self) -> None:
        self._graph: Optional[ArchitectureGraph] = None

    def publish(self, graph: ArchitectureGraph) -> None:
        self._graph = graph

    def current(self) -> Optional[ArchitectureGraph]:
        return self._graph
