from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class BootPlan:
    """
    Ordered execution plan for platform startup.
    """

    components: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    errors: list[str] = field(default_factory=list)

    def ready(self) -> bool:
        return len(self.errors) == 0
