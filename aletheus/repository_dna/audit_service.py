from __future__ import annotations

from pathlib import Path

from .audit_models import RepositoryDNAAuditReport
from .audit_scanner import RepositoryDNAScanner
from .collision_auditor import RepositoryDNACollisionAuditor


class RepositoryDNAAuditService:
    """Repository DNA Audit Engine.

    Repository DNA knows what exists.
    """

    authority = "Repository DNA™"
    family = "Platform Intelligence"
    knows = "Repository inventory and architectural genealogy"

    def __init__(
        self,
        scanner: RepositoryDNAScanner | None = None,
        collision_auditor: RepositoryDNACollisionAuditor | None = None,
    ) -> None:
        self.scanner = scanner or RepositoryDNAScanner()
        self.collision_auditor = collision_auditor or RepositoryDNACollisionAuditor()

    def audit(self, aletheus_root: Path) -> RepositoryDNAAuditReport:
        records = self.scanner.scan_subsystems(aletheus_root)
        collisions = self.collision_auditor.audit(records)

        return RepositoryDNAAuditReport(
            root=str(aletheus_root),
            subsystem_count=len(records),
            python_file_count=self.scanner.count_python_files(aletheus_root),
            subsystems=records,
            collision_candidates=collisions,
        )

    def write_report(self, aletheus_root: Path, output_path: Path) -> RepositoryDNAAuditReport:
        report = self.audit(aletheus_root)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report.to_markdown(), encoding="utf-8")
        return report
