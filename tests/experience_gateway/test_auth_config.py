from __future__ import annotations

import pytest

from aletheus.experience_gateway.security.auth_config import (
    AuthenticationConfig,
)


def test_local_mode_requires_no_oidc_values() -> None:
    config = AuthenticationConfig(mode="local")

    assert config.mode == "local"


def test_oidc_mode_requires_issuer() -> None:
    with pytest.raises(ValueError):
        AuthenticationConfig(
            mode="oidc",
            audience="api://aletheus",
            jwks_url=("https://example.test/v1/keys"),
        )


def test_oidc_mode_accepts_complete_configuration() -> None:
    config = AuthenticationConfig(
        mode="oidc",
        issuer=("https://example.test/oauth2/default"),
        audience="api://aletheus",
        jwks_url=("https://example.test/oauth2/default/v1/keys"),
    )

    assert config.algorithms == ("RS256",)
