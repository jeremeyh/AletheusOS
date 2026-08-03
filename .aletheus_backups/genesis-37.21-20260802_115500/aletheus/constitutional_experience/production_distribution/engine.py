from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from pathlib import Path

from .models import ArtifactClass, BuildArtifact, DistributionPlan


class ExperienceDistributionEngine:
    """Plans, validates, and assembles Genesis 37 experience distributions."""

    REQUIRED_ROOTS = (
        "core",
        "components",
        "applications",
        "config",
        "manifests",
    )

    def canonical_plan(self) -> DistributionPlan:
        return DistributionPlan(
            package_name="AletheusOS-Genesis37-CoreUI",
            version="1.0.0-GA",
            artifacts=[
                BuildArtifact(
                    "info_physics",
                    "rust/info_physics",
                    "core/physics/info_physics_core.wasm",
                    ArtifactClass.WASM,
                ),
                BuildArtifact(
                    "info_physics_bg",
                    "rust/info_physics",
                    "core/physics/info_physics_bg.wasm",
                    ArtifactClass.WASM,
                    dependencies=("info_physics",),
                ),
                BuildArtifact(
                    "axiomux_renderer",
                    "rust/axiomux_renderer",
                    "core/renderer/axiom_ux_renderer.wasm",
                    ArtifactClass.WASM,
                    dependencies=("info_physics",),
                ),
                BuildArtifact(
                    "particle_system",
                    "assets/shaders/particle_system.wgsl",
                    "core/renderer/wgsl/particle_system.wgsl",
                    ArtifactClass.WGSL,
                    dependencies=("axiomux_renderer",),
                ),
                BuildArtifact(
                    "dynamic_glass",
                    "assets/shaders/dynamic_glass.wgsl",
                    "core/renderer/wgsl/dynamic_glass.wgsl",
                    ArtifactClass.WGSL,
                    dependencies=("axiomux_renderer",),
                ),
                BuildArtifact(
                    "topological_mesh",
                    "assets/shaders/topological_mesh.wgsl",
                    "core/renderer/wgsl/topological_mesh.wgsl",
                    ArtifactClass.WGSL,
                    dependencies=("axiomux_renderer",),
                ),
                BuildArtifact(
                    "lighting_environment",
                    "assets/shaders/lighting_environment.wgsl",
                    "core/renderer/wgsl/lighting_environment.wgsl",
                    ArtifactClass.WGSL,
                    dependencies=("axiomux_renderer",),
                ),
                BuildArtifact(
                    "hyperbolic_navigation",
                    "rust/hyperbolic_engine",
                    "core/navigation/hyperbolic_engine.wasm",
                    ArtifactClass.WASM,
                    dependencies=("info_physics",),
                ),
                BuildArtifact(
                    "liquid_ui",
                    "ui/components/liquid_ui",
                    "components/liquid_ui",
                    ArtifactClass.COMPONENT,
                    dependencies=("axiomux_renderer",),
                ),
                BuildArtifact(
                    "workspace_composer",
                    "ui/components/workspace_composer",
                    "components/workspace_composer",
                    ArtifactClass.COMPONENT,
                    dependencies=("liquid_ui",),
                ),
                BuildArtifact(
                    "founder_observatory",
                    "ui/applications/founder_observatory",
                    "applications/founder_observatory",
                    ArtifactClass.APPLICATION,
                    dependencies=("workspace_composer",),
                    founder_restricted=True,
                ),
                BuildArtifact(
                    "mission_workspaces",
                    "ui/applications/mission_workspaces",
                    "applications/mission_workspaces",
                    ArtifactClass.APPLICATION,
                    dependencies=("workspace_composer",),
                ),
                BuildArtifact(
                    "workspace_templates",
                    "config/workspace_templates.json",
                    "config/workspace_templates.json",
                    ArtifactClass.CONFIG,
                ),
                BuildArtifact(
                    "instrument_registry",
                    "config/instrument_registry.json",
                    "config/instrument_registry.json",
                    ArtifactClass.CONFIG,
                ),
                BuildArtifact(
                    "physics_rulesets",
                    "config/physics_rulesets.json",
                    "config/physics_rulesets.json",
                    ArtifactClass.CONFIG,
                ),
            ],
        )

    def validate_distribution_root(self, root: Path) -> list[str]:
        return [
            f"missing distribution root: {required}"
            for required in self.REQUIRED_ROOTS
            if not (root / required).exists()
        ]

    def sha256(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def checksum_index(self, files: Iterable[Path], root: Path) -> dict[str, str]:
        return {
            str(path.relative_to(root)): self.sha256(path)
            for path in sorted(files)
            if path.is_file()
        }

    def write_plan(self, output: Path) -> None:
        plan = self.canonical_plan()
        errors = plan.validate()
        if errors:
            raise ValueError("; ".join(errors))
        payload = {
            "packageName": plan.package_name,
            "version": plan.version,
            "artifacts": [
                {
                    "id": artifact.artifact_id,
                    "sourcePath": artifact.source_path,
                    "outputPath": artifact.output_path,
                    "artifactClass": artifact.artifact_class.value,
                    "dependencies": list(artifact.dependencies),
                    "required": artifact.required,
                    "founderRestricted": artifact.founder_restricted,
                }
                for artifact in plan.artifacts
            ],
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2) + "\n")
