import pytest

from aletheus.strategic.span import SPANConfig


def test_span_config_rejects_invalid_confidence() -> None:
    config = SPANConfig(minimum_recommendation_confidence=1.5)

    with pytest.raises(ValueError):
        config.validate()
