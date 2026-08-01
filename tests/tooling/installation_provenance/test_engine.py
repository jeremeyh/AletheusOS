from aletheus.tooling.installation_provenance.engine import Engine


def test_provenance_entry(tmp_path) -> None:
    installer = tmp_path / "installer.py"
    installer.write_text("x", encoding="utf-8")
    entry = Engine(tmp_path / "out").append(
        release="1",
        commit="c",
        installer=installer,
        certification="ok",
        rollback_point="r",
        runtime_compatibility="yes",
    )
    assert entry["release"] == "1"
    assert len(entry["installer_hash"]) == 64
