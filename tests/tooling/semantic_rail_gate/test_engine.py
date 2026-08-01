import json

from aletheus.tooling.semantic_rail_gate.engine import Engine


def test_gate_passes_resolved_parallel_state(tmp_path) -> None:
    roots = tmp_path / "roots.json"
    rails = tmp_path / "rails.json"
    forks = tmp_path / "forks.json"
    continuity = tmp_path / "continuity.json"
    roots.write_text(json.dumps({"resolved_count": 1, "unresolved_roots": []}))
    rails.write_text(json.dumps({"parallel_in_out_enabled": True, "paired_rails": 1}))
    forks.write_text(json.dumps({"fork_count": 0}))
    continuity.write_text(json.dumps({"decision": "pass"}))
    report = Engine(roots, rails, forks, continuity, tmp_path / "out").build()
    assert report["decision"] == "pass"
