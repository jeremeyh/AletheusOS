from aletheus.card_hawk_navigation.experience_mesh.engine import Engine


def test_mesh():
    assert Engine().describe()["nodeCount"] >= 10
