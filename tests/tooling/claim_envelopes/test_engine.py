import json

from aletheus.tooling.claim_envelopes.engine import Engine


def test_duplicate_claim_is_enveloped(tmp_path) -> None:
    catalog = tmp_path / "catalog.json"
    roots = tmp_path / "roots.json"
    catalog.write_text(
        json.dumps(
            {
                "entries": [
                    {"name": "A", "authority": "Owns X"},
                    {"name": "B", "authority": "Owns X"},
                ]
            }
        )
    )
    roots.write_text(json.dumps({"resolved_count": 1}))
    report = Engine(catalog, roots, tmp_path / "out").build()
    assert report["ambivalent_claim_count"] == 1
