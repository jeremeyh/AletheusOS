import pytest
from aletheus.core import Identity, Result
from aletheus.sdk.evidence import Evidence


def test_identity_requires_name():
    with pytest.raises(ValueError):
        Identity(name="", kind="mission")


def test_result_ok():
    assert Result.ok({"status": "success"}).success is True


def test_evidence_validates_confidence():
    with pytest.raises(ValueError):
        Evidence("Invalid", "test", 1.5)
