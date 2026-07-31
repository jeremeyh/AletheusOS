from __future__ import annotations

from aletheus.runtime_platform.topology.dependency_graph import (
    DependencyGraph,
    DependencyGraphError,
)

from .runtime_manifest import RuntimeManifest


class RuntimeManifestValidator:
    """
    Validates runtime manifests before runtime composition.

    Validation responsibilities:

    • duplicate detection
    • supported entry kinds
    • dependency validation
    • dependency cycle detection
    """

    _SUPPORTED_KINDS = frozenset(
        {
            "domain",
            "service",
            "component",
            "provider",
        }
    )

    def validate(
        self,
        manifest: RuntimeManifest,
    ) -> tuple[str, ...]:
        errors: list[str] = []

        names = manifest.names()

        if len(names) != len(set(names)):
            errors.append("Manifest contains duplicate entry names.")

        graph = DependencyGraph()

        for entry in manifest.entries:
            if entry.kind not in self._SUPPORTED_KINDS:
                errors.append(f"Unsupported manifest kind: {entry.kind}")

            graph.add(
                entry.name,
                entry.dependencies,
            )

        try:
            graph.validate()

        except DependencyGraphError as exc:
            errors.append(str(exc))

        return tuple(errors)

    def assert_valid(
        self,
        manifest: RuntimeManifest,
    ) -> None:

        errors = self.validate(manifest)

        if errors:
            raise ValueError("Invalid runtime manifest: " + "; ".join(errors))
