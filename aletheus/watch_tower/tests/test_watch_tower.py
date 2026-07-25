from aletheus.watch_tower import bootstrap_watch_tower


def test_verify():
    assert bootstrap_watch_tower().verify().passed
