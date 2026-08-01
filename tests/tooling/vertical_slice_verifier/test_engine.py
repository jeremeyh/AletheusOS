import json

from aletheus.tooling.vertical_slice_verifier.engine import Engine


def test_vertical_slice_connects(tmp_path) -> None:
    paths = tmp_path / "paths.json"
    touchpoints = tmp_path / "touchpoints.json"
    paths.write_text(json.dumps({"nodes": ["A"]}))
    touchpoints.write_text(
        json.dumps({"touchpoints": [{"id": "x"}], "touchpoint_count": 1})
    )
    result = Engine(paths, touchpoints, tmp_path / "out").build()
    assert result["top_to_bottom_connected"] is True
