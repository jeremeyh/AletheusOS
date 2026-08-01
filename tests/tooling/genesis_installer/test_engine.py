from pathlib import Path

from aletheus.tooling.genesis_installer.engine import InstallerEngine
from aletheus.tooling.genesis_installer.models import ReleaseManifest


def test_checksum_and_dry_run(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    package = tmp_path / "package"
    repository.mkdir()
    (package / "target").mkdir(parents=True)
    file = package / "target/example.txt"
    file.write_text("verified", encoding="utf-8")

    engine = InstallerEngine(repository)
    checksum = engine.sha256(file)
    manifest = ReleaseManifest(
        release_id="genesis-test",
        version="1.0.0",
        title="Test",
        commit_message="Test",
        package_root=package,
        targets=["target"],
    )
    result = engine.install(
        manifest,
        checksums={"target/example.txt": checksum},
        dry_run=True,
    )
    assert result["status"] == "dry_run_complete"
