import json

from aletheus.tooling.parallel_rails.engine import Engine


def test_parallel_rails_enable_when_counts_match(tmp_path) -> None:
    inbound = tmp_path / "in.json"
    outbound = tmp_path / "out.json"
    inbound.write_text(json.dumps({"rail_count": 2}))
    outbound.write_text(json.dumps({"rail_count": 2}))
    report = Engine(inbound, outbound, tmp_path / "result").build()
    assert report["parallel_in_out_enabled"] is True
