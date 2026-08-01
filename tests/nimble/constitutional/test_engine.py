from aletheus.nimble.constitutional.engine import Engine


def test_reserved_instruments() -> None:
    assert all(item.reserved for item in Engine().catalog())
