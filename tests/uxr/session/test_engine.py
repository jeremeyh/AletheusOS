from aletheus.uxr.session.engine import Engine


def test_x():
    e = Engine()
    e.create(session_id="s", user_id="u", experience_id="x")
    assert e.update("s", {"a": 1}).state["a"] == 1
