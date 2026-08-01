from aletheus.uxr.guardrails.engine import Engine
from aletheus.uxr.guardrails.models import Experience, Node, RuntimeMeta


def test_x():
    e = Experience(
        "23",
        RuntimeMeta("T", "summary", {}),
        Node("Unknown", {"rawHtml": "x"}),
        "e",
        "1",
    )
    s, f = Engine().sanitize(e, {"LayoutContainer", "BannerAlert"})
    assert s.root.component == "BannerAlert" and f
