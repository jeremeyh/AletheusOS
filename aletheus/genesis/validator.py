from __future__ import annotations

from .models import GenesisPackageSpec


class GenesisValidator:
    """Validates Genesis Package specs before construction."""

    def validate(self, spec: GenesisPackageSpec) -> list[str]:
        errors: list[str] = []

        if not spec.gp_id.startswith("GP-"):
            errors.append("gp_id must start with GP-")

        if not spec.title:
            errors.append("title is required")

        if not spec.authority:
            errors.append("authority is required")

        if not spec.family:
            errors.append("family is required")

        if not spec.package_name:
            errors.append("package_name is required")

        if spec.files_to_delete:
            errors.append("deletions require explicit migration approval")

        return errors
