import json

from aletheus.tooling.platform_continuity_gate.engine import Engine


def test_continuity_gate_passes_connected_platform(tmp_path) -> None:
    vertical = tmp_path / "vertical.json"
    horizontal = tmp_path / "horizontal.json"
    access = tmp_path / "access.json"
    governance = tmp_path / "governance.json"
    vertical.write_text(json.dumps({"top_to_bottom_connected": True}))
    horizontal.write_text(json.dumps({"horizontal_mesh_connected": True}))
    access.write_text(json.dumps({"access_module_count": 1}))
    governance.write_text(json.dumps({"decision": "pass"}))
    result = Engine(vertical, horizontal, access, governance, tmp_path / "out").build()
    assert result["decision"] == "pass"
