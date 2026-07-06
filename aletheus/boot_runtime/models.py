from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class BootResult:
    component_id: str
    name: str
    success: bool
    message: str = ""


@dataclass(slots=True)
class BootReport:
    genesis: str = "13.9"
    version: str = "0.1.0"

    results: list[BootResult] = field(default_factory=list)

    @property
    def successful(self):
        return sum(result.success for result in self.results)

    @property
    def failed(self):
        return len(self.results) - self.successful

    @property
    def passed(self):
        return self.failed == 0

    def to_dict(self):

        return {
            "genesis": self.genesis,
            "version": self.version,
            "passed": self.passed,
            "successful": self.successful,
            "failed": self.failed,
            "results": [
                {
                    "component_id": r.component_id,
                    "name": r.name,
                    "success": r.success,
                    "message": r.message,
                }
                for r in self.results
            ],
        }
