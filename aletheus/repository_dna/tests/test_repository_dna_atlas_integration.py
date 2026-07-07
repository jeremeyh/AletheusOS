from pathlib import Path

from aletheus.atlas.repository_dna_service import RepositoryAwareAtlasService


def test_atlas_consumes_repository_dna_inventory(tmp_path: Path):
    root = tmp_path / "aletheus"
    (root / "runtime").mkdir(parents=True)
    (root / "memory_mesh").mkdir(parents=True)
    (root / "runtime" / "__init__.py").write_text("", encoding="utf-8")

    service = RepositoryAwareAtlasService()
    report = service.discover_from_repository_dna(root)

    assert report.snapshot.subsystem_count == 2
    assert service.graph() is not None
