from aletheus.uxr.layout.engine import Engine
from aletheus.uxr.layout.models import Experience, Node, RuntimeMeta


def test_x():
    e = Experience(
        "23", RuntimeMeta("T", "summary", {}), Node("LayoutContainer", {}), "e", "1"
    )
    assert (
        Engine().adapt(e, viewport_width=500, viewport_height=900).root.props["columns"]
        == 1
    )
