from repository.engine import RepositoryStewardshipEngine


def test_smoke():
    assert RepositoryStewardshipEngine().inspect()["status"] == "scaffold"
