import json

from aletheus.tooling.structural_hardening.engine import Engine


def test_hardening_disallows_parallel_layer(tmp_path) -> None:
    roots = tmp_path / "roots.json"
    cycles = tmp_path / "cycles.json"
    continuity = tmp_path / "continuity.json"
    roots.write_text(json.dumps({"ambiguous_roots": ["X"]}))
    cycles.write_text(json.dumps({"unclassified_cycles": []}))
    continuity.write_text(json.dumps({"decision": "warn"}))
    report = Engine(roots, cycles, continuity, tmp_path / "out").build()
    assert report["parallel_layer_created"] is False
