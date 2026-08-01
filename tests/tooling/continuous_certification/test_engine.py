from aletheus.tooling.continuous_certification.engine import Engine


def test_continuous_certification(tmp_path) -> None:
    report = Engine().certify({"score": 100}, tmp_path)
    assert report["status"] == "certified"
