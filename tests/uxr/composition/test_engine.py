from aletheus.uxr.composition.engine import Engine


def test_x():
    e = Engine().compose(
        title="ROI",
        layout_type="dashboard",
        intent_name="compare",
        catalog={"LayoutContainer", "MetricsCard", "BannerAlert"},
        data={"metrics": [{"title": "ROI", "value": "17%"}]},
    )
    assert e.root.children[0].component == "MetricsCard"
