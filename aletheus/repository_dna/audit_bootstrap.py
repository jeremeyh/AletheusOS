from __future__ import annotations

from .audit_service import RepositoryDNAAuditService


def bootstrap_repository_dna_audit_service() -> RepositoryDNAAuditService:
    return RepositoryDNAAuditService()
