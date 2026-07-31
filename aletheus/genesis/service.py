from __future__ import annotations

from pathlib import Path

from .models import GenesisPackageResult, GenesisPackageSpec
from .package_builder import GenesisPackageBuilder


class GenesisService:
    """
    Service facade for Genesis™ Platform Constructor.

    Genesis knows conformant scaffolding.
    """

    authority = "Genesis™"
    family = "Creation"
    knows = "conformant scaffolding"

    def __init__(self, builder: GenesisPackageBuilder | None = None) -> None:
        self.builder = builder or GenesisPackageBuilder()

    def build_package(
        self, spec: GenesisPackageSpec, output_root: Path
    ) -> GenesisPackageResult:
        return self.builder.build(spec, output_root)
