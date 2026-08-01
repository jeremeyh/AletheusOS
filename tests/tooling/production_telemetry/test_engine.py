from aletheus.tooling.production_telemetry.engine import Engine


def test_production_telemetry() -> None:
    report = Engine().summarize(({"latency": 1.0}, {"latency": 3.0}))
    assert report["aggregates"]["latency"] == 2.0
