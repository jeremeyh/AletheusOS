import json

from aletheus.tooling.ecosystem_catalog.engine import EcosystemCatalogEngine


def test_catalog_merges_duplicate_names(tmp_path) -> None:
    base = tmp_path / "base.json"
    expansion = tmp_path / "expansion.json"
    base.write_text(json.dumps({"entries": [{"name": "Kinekt", "aliases": []}]}))
    expansion.write_text(
        json.dumps({"entries": [{"name": "Kinekt™", "aliases": ["Kinekt"]}]})
    )
    result = EcosystemCatalogEngine(base, expansion, tmp_path / "out").build()
    assert len(result["entries"]) == 1
