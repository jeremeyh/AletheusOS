from __future__ import annotations

from .manifest import build_manifest
from .models import GenesisPackagePlan, GenesisPackageSpec


class GenesisPlanner:
    """
    Produces a construction plan before code is generated.

    Genesis does not merely write files; it plans constitutional construction.
    """

    def plan(self, spec: GenesisPackageSpec) -> GenesisPackagePlan:
        verification = [
            "Package imports successfully",
            "Integration Manifest exists",
            "ENGINEERING_NOTES.md exists",
            "VERIFY.md exists",
            "ROLLBACK.md exists",
            "Collision check completed",
            "Watch Tower verification completed",
        ]

        rollback = [
            "Remove added package files",
            "Revert modified files if patches were applied",
            "Re-run verification to confirm clean rollback",
        ]

        return GenesisPackagePlan(
            spec=spec,
            manifest=build_manifest(spec),
            verification_steps=verification,
            rollback_steps=rollback,
        )
