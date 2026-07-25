from __future__ import annotations

from .models import GenesisPackageSpec


class GenesisRegistry:
    """Tracks Genesis Package specs."""

    def __init__(self) -> None:
        self._packages: dict[str, GenesisPackageSpec] = {}

    def register(self, spec: GenesisPackageSpec) -> None:
        self._packages[spec.gp_id] = spec

    def get(self, gp_id: str) -> GenesisPackageSpec | None:
        return self._packages.get(gp_id)

    def all(self) -> list[GenesisPackageSpec]:
        return list(self._packages.values())
