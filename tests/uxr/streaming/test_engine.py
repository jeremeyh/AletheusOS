from aletheus.uxr.streaming.engine import Engine
from aletheus.uxr.streaming.models import Experience, Node, RuntimeMeta


def test_x():
    e = Experience(
        "23",
        RuntimeMeta("T", "summary", {}),
        Node(
            "LayoutContainer",
            {},
            children=(
                Node("BannerAlert", {}),
                Node("BannerAlert", {}),
                Node("BannerAlert", {}),
            ),
        ),
        "e",
        "1",
    )
    assert len(Engine().chunks(e, chunk_size=2)) == 2
