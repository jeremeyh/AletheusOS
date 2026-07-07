from pathlib import Path

from aletheus.atlas import AtlasService


def test_atlas_discovers_subsystems(tmp_path: Path):
    root = tmp_path / "aletheus"
    (root / "runtime").mkdir(parents=True)
    (root / "memory_mesh").mkdir(parents=True)
    (root / "runtime" / "__init__.py").write_text("", encoding="utf-8")
    (root / "memory_mesh" / "__init__.py").write_text("", encoding="utf-8")

    service = AtlasService()
    report = service.discover(root)

    assert report.snapshot.subsystem_count == 2
    assert service.health().graph_loaded is True
    assert service.metrics()["atlas_node_count"] >= 2
