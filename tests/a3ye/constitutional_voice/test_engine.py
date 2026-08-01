from aletheus.a3ye.constitutional_voice.engine import Engine
from aletheus.a3ye.constitutional_voice.models import DeterminationVector


def test_x() -> None:
    result = Engine().compose(
        thesis="Likely",
        determination=DeterminationVector(0.9, 1, 0.8, 0.9, 0.1, 0.88),
        evidence_summary="strong",
        uncertainty_summary="variance",
    )
    assert result["unconcealedTruth"] is True
