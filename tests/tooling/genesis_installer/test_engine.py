from pathlib import Path

from aletheus.tooling.genesis_installer.engine import InstallerEngine
from aletheus.tooling.genesis_installer.models import (
    ReleaseManifest,
    ReleaseTarget,
)


def test_atomic_dry_run_and_checksum(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    package = tmp_path / "package"
    repository.mkdir()
    (repository / ".git").mkdir()
    (repository / "aletheus").mkdir()
    (package / "aletheus/tooling/example").mkdir(parents=True)
    (package / "aletheus/__init__.py").write_text("", encoding="utf-8")
    (package / "aletheus/tooling/__init__.py").write_text("", encoding="utf-8")
    source = package / "aletheus/tooling/example/engine.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")

    manifest = ReleaseManifest(
        release_id="genesis-test",
        version="1.0.0",
        title="Test",
        commit_message="Test",
        package_root=package,
        targets=(
            ReleaseTarget(
                source="aletheus/tooling/example",
                destination="aletheus/tooling/example",
            ),
        ),
    )
    engine = InstallerEngine(repository)
    result = engine.install(
        manifest,
        checksums={"aletheus/tooling/example/engine.py": engine.sha256(source)},
        dry_run=True,
    )
    assert result["status"] == "dry_run_complete"
