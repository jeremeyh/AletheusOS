from __future__ import annotations

from pathlib import Path

try:
    from .audit_models import SubsystemRecord
    from .audit_service import RepositoryDNAAuditService
except Exception:  # pragma: no cover - compatibility fallback
    RepositoryDNAAuditService = None
    SubsystemRecord = None


class RepositoryDNAInventoryProvider:
    """Canonical repository inventory provider.

    Repository DNA answers: what exists?
    Atlas consumes this inventory to answer: how does it connect?
    """

    authority = "Repository DNA™"
    family = "Platform Intelligence"
    knows = "repository inventory"

    def __init__(self, audit_service=None) -> None:
        if audit_service is not None:
            self.audit_service = audit_service
        elif RepositoryDNAAuditService is not None:
            self.audit_service = RepositoryDNAAuditService()
        else:
            self.audit_service = None

    def inventory(self, aletheus_root: Path):
        if self.audit_service is None:
            return self._fallback_inventory(aletheus_root)
        return self.audit_service.audit(aletheus_root).subsystems

    def _fallback_inventory(self, aletheus_root: Path):
        records = []
        for child in sorted(aletheus_root.iterdir()):
            if child.is_dir() and not child.name.startswith("__"):
                records.append(
                    {
                        "name": child.name,
                        "path": str(child),
                        "python_files": len(list(child.rglob("*.py"))),
                        "family": "Unclassified",
                    }
                )
        return records
