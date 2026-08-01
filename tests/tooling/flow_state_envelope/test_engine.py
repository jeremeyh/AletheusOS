import json

from aletheus.tooling.flow_state_envelope.engine import Engine


def test_flow_state_is_enveloped(tmp_path) -> None:
    rails = tmp_path / "rails.json"
    claims = tmp_path / "claims.json"
    rails.write_text(
        json.dumps(
            {"flow_state": "full_duplex_bounded", "parallel_in_out_enabled": True}
        )
    )
    claims.write_text(json.dumps({"ambivalent_claim_count": 1}))
    report = Engine(rails, claims, tmp_path / "out").build()
    assert report["state"] == "enveloped"
