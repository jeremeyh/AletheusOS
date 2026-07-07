from pathlib import Path

from aletheus.genesis import (
    GenesisClassification,
    GenesisPackageSpec,
    GenesisRisk,
    GenesisService,
)


def test_genesis_builds_package(tmp_path: Path):
    service = GenesisService()
    spec = GenesisPackageSpec(
        gp_id="GP-TEST",
        title="Test Package",
        classification=GenesisClassification.SERVICE,
        authority="Genesis™",
        family="Creation",
        package_name="test_package",
        summary="A test package.",
        risk=GenesisRisk.LOW,
        files_to_add=["aletheus/test_package/__init__.py"],
    )

    result = service.build_package(spec, tmp_path)

    assert result.ready is True
    assert (tmp_path / "GP-TEST" / "manifest.json").exists()
    assert (tmp_path / "GP-TEST" / "aletheus/test_package/__init__.py").exists()
