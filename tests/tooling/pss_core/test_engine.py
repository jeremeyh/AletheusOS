from aletheus.tooling.pss_core.engine import Engine
from aletheus.tooling.pss_core.models import Metric


def test_pss_core() -> None:
    report = Engine().evaluate((Metric("x", 100.0),))
    assert report.score == 100.0
    assert report.status == "production_certified"
