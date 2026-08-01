from aletheus.constitutional_ui.projection_neutrality.engine import Engine, Request


def test_x():
    assert Engine().project(
        {"valid": True}, Request("executive_report", "c_level", "high")
    )["projectionNeutralityPreserved"]
