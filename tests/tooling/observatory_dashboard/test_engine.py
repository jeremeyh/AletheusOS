import json

from aletheus.tooling.observatory_dashboard.engine import DashboardEngine


def test_dashboard_builds_cards(tmp_path) -> None:
    observatory = tmp_path / "observatory.json"
    observatory.write_text(json.dumps({"health_score": 50, "authority_coverage": 20}))
    dashboard = DashboardEngine(
        {
            "observatory": observatory,
            "mission_control": tmp_path / "missing1.json",
            "com": tmp_path / "missing2.json",
            "twin": tmp_path / "missing3.json",
        },
        tmp_path / "out",
    ).build()
    assert len(dashboard["cards"]) == 5
