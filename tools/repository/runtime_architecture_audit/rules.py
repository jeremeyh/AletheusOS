from __future__ import annotations

from dataclasses import dataclass, field

RUNTIME_PREFIX = "aletheus.runtime"


@dataclass(frozen=True, slots=True)
class ArchitectureLayer:
    """One logical runtime architecture layer."""

    name: str
    package_prefixes: tuple[str, ...]
    rank: int

    def owns(self, module_name: str) -> bool:
        return any(
            module_name == prefix or module_name.startswith(f"{prefix}.")
            for prefix in self.package_prefixes
        )


@dataclass(frozen=True, slots=True)
class ForbiddenDependency:
    """An explicit dependency relationship that must never occur."""

    source_prefix: str
    target_prefix: str
    reason: str

    def matches(self, source: str, target: str) -> bool:
        source_matches = source == self.source_prefix or source.startswith(
            f"{self.source_prefix}."
        )
        target_matches = target == self.target_prefix or target.startswith(
            f"{self.target_prefix}."
        )

        return source_matches and target_matches


@dataclass(frozen=True, slots=True)
class ArchitectureRules:
    """Canonical runtime dependency rules."""

    layers: tuple[ArchitectureLayer, ...]
    forbidden_dependencies: tuple[ForbiddenDependency, ...]
    allowed_upward_dependencies: frozenset[tuple[str, str]] = field(
        default_factory=frozenset
    )

    def layer_for(
        self,
        module_name: str,
    ) -> ArchitectureLayer | None:
        matching_layers = [layer for layer in self.layers if layer.owns(module_name)]

        if not matching_layers:
            return None

        # Prefer the most specific package match.
        return max(
            matching_layers,
            key=lambda layer: max(
                len(prefix)
                for prefix in layer.package_prefixes
                if module_name == prefix or module_name.startswith(f"{prefix}.")
            ),
        )


DEFAULT_ARCHITECTURE_RULES = ArchitectureRules(
    layers=(
        ArchitectureLayer(
            name="composition",
            package_prefixes=(f"{RUNTIME_PREFIX}.composition",),
            rank=0,
        ),
        ArchitectureLayer(
            name="core",
            package_prefixes=(f"{RUNTIME_PREFIX}.core",),
            rank=1,
        ),
        ArchitectureLayer(
            name="kernel",
            package_prefixes=(
                f"{RUNTIME_PREFIX}.kernel",
                f"{RUNTIME_PREFIX}.executive",
            ),
            rank=2,
        ),
        ArchitectureLayer(
            name="boot",
            package_prefixes=(
                f"{RUNTIME_PREFIX}.boot",
                f"{RUNTIME_PREFIX}.boot_director",
                f"{RUNTIME_PREFIX}.boot_phases",
                f"{RUNTIME_PREFIX}.boot_pipeline",
                f"{RUNTIME_PREFIX}.bootstrap",
                f"{RUNTIME_PREFIX}.command_bootstrap",
            ),
            rank=3,
        ),
        ArchitectureLayer(
            name="orchestration",
            package_prefixes=(
                f"{RUNTIME_PREFIX}.orchestration",
                f"{RUNTIME_PREFIX}.lifecycle",
                f"{RUNTIME_PREFIX}.registration",
                f"{RUNTIME_PREFIX}.managers",
                f"{RUNTIME_PREFIX}.scheduler",
                f"{RUNTIME_PREFIX}.pipeline",
                f"{RUNTIME_PREFIX}.workflow",
            ),
            rank=4,
        ),
        ArchitectureLayer(
            name="services",
            package_prefixes=(
                f"{RUNTIME_PREFIX}.services",
                f"{RUNTIME_PREFIX}.service_mesh",
                f"{RUNTIME_PREFIX}.registry",
                f"{RUNTIME_PREFIX}.providers",
                f"{RUNTIME_PREFIX}.container",
                f"{RUNTIME_PREFIX}.capabilities",
            ),
            rank=5,
        ),
        ArchitectureLayer(
            name="domains",
            package_prefixes=(
                f"{RUNTIME_PREFIX}.domains",
                f"{RUNTIME_PREFIX}.applications",
                f"{RUNTIME_PREFIX}.handlers",
                f"{RUNTIME_PREFIX}.registrations",
                f"{RUNTIME_PREFIX}.commands",
                f"{RUNTIME_PREFIX}.commands_v2",
            ),
            rank=6,
        ),
        ArchitectureLayer(
            name="contracts",
            package_prefixes=(
                f"{RUNTIME_PREFIX}.contracts",
                f"{RUNTIME_PREFIX}.context",
                f"{RUNTIME_PREFIX}.events",
            ),
            rank=7,
        ),
    ),
    forbidden_dependencies=(
        ForbiddenDependency(
            source_prefix=f"{RUNTIME_PREFIX}.kernel",
            target_prefix=f"{RUNTIME_PREFIX}.composition",
            reason=("The runtime kernel may not depend upon its composition root."),
        ),
        ForbiddenDependency(
            source_prefix=f"{RUNTIME_PREFIX}.domains",
            target_prefix=f"{RUNTIME_PREFIX}.core",
            reason=("Runtime domains may not depend directly upon runtime.core."),
        ),
        ForbiddenDependency(
            source_prefix=f"{RUNTIME_PREFIX}.services",
            target_prefix=f"{RUNTIME_PREFIX}.composition",
            reason=("Services may not depend upon runtime composition."),
        ),
        ForbiddenDependency(
            source_prefix=f"{RUNTIME_PREFIX}.managers",
            target_prefix=f"{RUNTIME_PREFIX}.composition",
            reason=("Runtime managers may not depend upon the composition root."),
        ),
        ForbiddenDependency(
            source_prefix=f"{RUNTIME_PREFIX}.contracts",
            target_prefix=f"{RUNTIME_PREFIX}.core",
            reason=("Runtime contracts must remain independent of runtime.core."),
        ),
    ),
    allowed_upward_dependencies=frozenset(
        {
            # Transitional compatibility allowances can be recorded here.
            #
            # Example:
            # (
            #     "aletheus.runtime.core",
            #     "aletheus.runtime.composition",
            # ),
        }
    ),
)
