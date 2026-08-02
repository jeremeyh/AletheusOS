from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ArtifactClass(StrEnum):
    WASM = "wasm"
    WGSL = "wgsl"
    COMPONENT = "component"
    APPLICATION = "application"
    CONFIG = "config"
    MANIFEST = "manifest"
    INSTALLER = "installer"


@dataclass(frozen=True, slots=True)
class BuildArtifact:
    artifact_id: str
    source_path: str
    output_path: str
    artifact_class: ArtifactClass
    dependencies: tuple[str, ...] = ()
    required: bool = True
    founder_restricted: bool = False


@dataclass(slots=True)
class DistributionPlan:
    package_name: str
    version: str
    artifacts: list[BuildArtifact] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors: list[str] = []
        ids: set[str] = set()
        outputs: set[str] = set()

        for artifact in self.artifacts:
            if artifact.artifact_id in ids:
                errors.append(f"duplicate artifact id: {artifact.artifact_id}")
            ids.add(artifact.artifact_id)

            if artifact.output_path in outputs:
                errors.append(f"duplicate output path: {artifact.output_path}")
            outputs.add(artifact.output_path)

            if artifact.output_path.startswith("/"):
                errors.append(f"output path must be relative: {artifact.output_path}")

        known = {artifact.artifact_id for artifact in self.artifacts}
        for artifact in self.artifacts:
            for dependency in artifact.dependencies:
                if dependency not in known:
                    errors.append(
                        f"{artifact.artifact_id} references unknown dependency {dependency}"
                    )

        return errors
