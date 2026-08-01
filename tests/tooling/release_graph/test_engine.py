import json

from aletheus.tooling.release_graph.engine import Engine


def test_release_graph(tmp_path) -> None:
    release = tmp_path / "r"
    release.mkdir()
    (release / "release-manifest.json").write_text(
        json.dumps(
            {
                "release_id": "a",
                "version": "1",
                "title": "A",
                "dependencies": [],
            }
        ),
        encoding="utf-8",
    )
    report = Engine(tmp_path, tmp_path / "out").build()
    assert report["release_count"] == 1
    assert report["cycle_free"] is True
