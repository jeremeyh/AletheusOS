from __future__ import annotations

from pathlib import Path

from .constructor import GenesisConstructor
from .models import GenesisPackageResult, GenesisPackageSpec
from .planner import GenesisPlanner
from .validator import GenesisValidator


class GenesisPackageBuilder:
    """High-level builder used by GenesisService."""

    def __init__(
        self,
        planner: GenesisPlanner | None = None,
        constructor: GenesisConstructor | None = None,
        validator: GenesisValidator | None = None,
    ) -> None:
        self.planner = planner or GenesisPlanner()
        self.constructor = constructor or GenesisConstructor()
        self.validator = validator or GenesisValidator()

    def build(
        self, spec: GenesisPackageSpec, output_root: Path
    ) -> GenesisPackageResult:
        errors = self.validator.validate(spec)
        if errors:
            raise ValueError("; ".join(errors))

        plan = self.planner.plan(spec)
        return self.constructor.construct(plan, output_root)
