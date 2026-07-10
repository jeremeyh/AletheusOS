from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class BootCandidate:
    component_id: str
    name: str
    priority: int = 100
    dependencies: list[str] = field(default_factory=list)
    verified: bool = False


@dataclass(slots=True)
class BootPlan:
    genesis: str = "13.8"
    version: str = "0.1.0"
    candidates: list[BootCandidate] = field(default_factory=list)

    def ready(self) -> bool:
        return all(candidate.verified for candidate in self.candidates)

    def ordered(self) -> list[BootCandidate]:
        return sorted(
            self.candidates,
            key=lambda candidate: candidate.priority,
        )

    def to_dict(self):
        return {
            "genesis": self.genesis,
            "version": self.version,
            "ready": self.ready(),
            "components": [
                {
                    "component_id": candidate.component_id,
                    "name": candidate.name,
                    "priority": candidate.priority,
                    "dependencies": candidate.dependencies,
                    "verified": candidate.verified,
                }
                for candidate in self.ordered()
            ],
        }
