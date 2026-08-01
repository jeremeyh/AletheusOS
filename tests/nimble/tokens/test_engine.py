from aletheus.nimble.tokens.engine import Engine, Token


def test_token_resolution() -> None:
    assert (
        Engine().resolve(
            (Token("color", "surface", "#000", "surface"),),
            namespace="color",
            name="surface",
        )
        == "#000"
    )
