from aletheus.uxr.intent.engine import Engine


def test_x():
    i = Engine().translate("acquisition ROI", user_role="c_level")
    assert i.layout_type == "dashboard" and "Risk" in i.capabilities
