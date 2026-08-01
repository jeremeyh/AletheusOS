from aletheus.uxr.schema.engine import Engine
from aletheus.uxr.schema.models import Experience, Node, RuntimeMeta


def test_x():
    e = Experience(
        "23", RuntimeMeta("T", "summary", {}), Node("LayoutContainer", {}), "e", "1"
    )
    assert Engine().validate(e, {"LayoutContainer"})["valid"]
