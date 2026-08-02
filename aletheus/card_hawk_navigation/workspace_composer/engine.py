from __future__ import annotations

from typing import ClassVar

from .models import WorkspacePriority, WorkspaceRegion


class Engine:
    MAX_PRIMARY_REGIONS: ClassVar[int] = 1
    MAX_TOTAL_REGIONS: ClassVar[int] = 6

    def compose(self, regions: tuple[WorkspaceRegion, ...]) -> dict[str, object]:
        findings = []
        primary = sum(1 for r in regions if r.priority == WorkspacePriority.PRIMARY)
        if primary > self.MAX_PRIMARY_REGIONS:
            findings.append("workspace can contain only one primary region")
        if len(regions) > self.MAX_TOTAL_REGIONS:
            findings.append("workspace exceeds maximum region count")
        return {
            "valid": not findings,
            "findings": findings,
            "regions": regions,
            "totalWeight": sum(r.weight for r in regions),
        }
