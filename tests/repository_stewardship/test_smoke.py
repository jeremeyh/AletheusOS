from aletheus.repository import RepositoryStewardshipEngine

def test_smoke():
    assert RepositoryStewardshipEngine().inspect()['status']=='scaffold'
