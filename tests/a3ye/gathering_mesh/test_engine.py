from aletheus.a3ye.gathering_mesh.engine import Engine, SourceResult


def test_x() -> None:
    assert (
        Engine().gather((SourceResult("s", "api", {}, 0.9, 10.0),))["sourceCount"] == 1
    )
