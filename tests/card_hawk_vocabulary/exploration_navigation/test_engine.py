from aletheus.card_hawk_vocabulary.exploration_navigation.engine import Engine


def test_navigation() -> None:
    assert Engine().resolve("Atlas").domain_family == "EXPLORATION_NAVIGATION"
