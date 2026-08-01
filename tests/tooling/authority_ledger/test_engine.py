import json

from aletheus.tooling.authority_ledger.engine import AuthorityLedgerEngine


def test_ledger_detects_maturity(tmp_path):
    files = {}
    for name, payload in {
        "catalog": {
            "entries": [
                {
                    "name": "Example",
                    "category": "x",
                    "parent": "x",
                    "authority": "Owns x",
                    "aliases": ["example"],
                    "mesh_connections": ["Council"],
                    "must_not_own": ["y"],
                }
            ]
        },
        "authority": {"capabilities": [{"name": "Example"}]},
        "registry": {},
        "twin": {},
        "graph": {},
        "governance": {},
    }.items():
        p = tmp_path / f"{name}.json"
        p.write_text(json.dumps(payload))
        files[name] = p
    (tmp_path / "example.py").write_text("# example")
    report = AuthorityLedgerEngine(
        files["catalog"],
        files["authority"],
        files["registry"],
        files["twin"],
        files["graph"],
        files["governance"],
        tmp_path,
        tmp_path / "out",
    ).build()
    assert report["entries"][0]["realized"] is True
