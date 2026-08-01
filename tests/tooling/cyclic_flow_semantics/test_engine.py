import json

from aletheus.tooling.cyclic_flow_semantics.engine import Engine


def test_bidirectional_cycle_is_detected(tmp_path) -> None:
    wiring = tmp_path / "wiring.json"
    wiring.write_text(
        json.dumps(
            {"routes": [{"source": "A", "target": "B"}, {"source": "B", "target": "A"}]}
        )
    )
    report = Engine(wiring, tmp_path / "out").build()
    assert report["cycle_group_count"] == 1
