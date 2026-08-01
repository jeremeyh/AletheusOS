import json

from aletheus.tooling.process_grid_consolidation.engine import Engine


def test_all_components_are_absorbed_without_removal(tmp_path) -> None:
    names = [
        "Semantic Rail Continuity Gate",
        "Full Platform Continuity Gate",
        "Vertical Slice Verifier",
        "Horizontal Mesh Verifier",
        "Runtime Diagnostics",
        "Runtime Observability",
        "Runtime Telemetry",
        "Architectural Governance",
    ]
    sources = {}
    for index, name in enumerate(names):
        path = tmp_path / f"{index}.json"
        path.write_text(json.dumps({"status": "ok"}))
        sources[name] = path
    report = Engine(sources, tmp_path / "out").build()
    assert report["absorbed_components"] == 8
    assert report["functionality_removed"] is False
