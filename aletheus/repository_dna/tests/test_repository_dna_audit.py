from pathlib import Path

from aletheus.repository_dna.audit_service import RepositoryDNAAuditService


def test_repository_dna_audit_detects_clusters(tmp_path: Path):
    root = tmp_path / "aletheus"
    (root / "kernel").mkdir(parents=True)
    (root / "kernel_v2").mkdir(parents=True)
    (root / "runtime").mkdir(parents=True)
    (root / "application_runtime").mkdir(parents=True)
    (root / "kernel" / "__init__.py").write_text("", encoding="utf-8")

    report = RepositoryDNAAuditService().audit(root)

    assert report.subsystem_count == 4
    assert report.python_file_count == 1
    assert any(c.cluster == "kernel" for c in report.collision_candidates)
    assert any(c.cluster == "runtime" for c in report.collision_candidates)
