import json

from aletheus.tooling.kinekt.integrity.trend import compare_previous


def test_trend_improved(tmp_path) -> None:
    baseline = tmp_path / "baseline.json"
    baseline.write_text(
        json.dumps({"total_score": 80}),
        encoding="utf-8",
    )

    trend, previous = compare_previous(90, baseline)

    assert trend == "improved"
    assert previous == 80
