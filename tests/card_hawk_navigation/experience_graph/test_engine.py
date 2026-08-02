from aletheus.card_hawk_navigation.experience_graph.engine import Engine


def test_route():
    assert Engine().route("field_vision", "marketplace")[-1] == "marketplace"
