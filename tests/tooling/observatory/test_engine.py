import json

from aletheus.tooling.observatory.engine import ObservatoryEngine


def test_observatory_aggregates_reports(tmp_path) -> None:
    health = tmp_path / "health.json"
    authority = tmp_path / "authority.json"
    twin = tmp_path / "twin.json"
    orchestration = tmp_path / "orchestration.json"

    health.write_text(json.dumps({"total_score": 50, "readiness": "not_ready"}))
    authority.write_text(
        json.dumps(
            {
                "module_assignments": {"a": "Kinekt"},
                "unresolved_modules": ["b"],
            }
        )
    )
    twin.write_text(json.dumps({"nodes": []}))
    orchestration.write_text(json.dumps({"units": [{}, {}]}))

    report = ObservatoryEngine(
        health,
        authority,
        twin,
        orchestration,
        tmp_path / "out",
    ).analyze()

    assert report.execution_units == 2
    assert report.alerts
