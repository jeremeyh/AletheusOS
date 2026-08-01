import json

from aletheus.tooling.forked_authority.engine import Engine


def test_forked_claims_build(tmp_path) -> None:
    claims = tmp_path / "claims.json"
    envelope = tmp_path / "envelope.json"
    claims.write_text(
        json.dumps({"claim_envelopes": [{"claim": "x", "envelope": {"A": "a"}}]})
    )
    envelope.write_text(json.dumps({"state": "enveloped"}))
    report = Engine(claims, envelope, tmp_path / "out").build()
    assert report["fork_count"] == 1
