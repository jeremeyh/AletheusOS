from __future__ import annotations

from typing import Any

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from aletheus.experience_gateway.security.auth_config import (
    AuthenticationConfig,
)
from aletheus.experience_gateway.security.oidc_authenticator import (
    AuthenticationFailure,
    OIDCPrincipalAuthenticator,
)


class FakeSigningKey:
    def __init__(
        self,
        key: Any,
    ) -> None:
        self.key = key


class FakeJWKClient:
    def __init__(
        self,
        public_key: Any,
    ) -> None:
        self._public_key = public_key

    def get_signing_key_from_jwt(
        self,
        token: str,
    ) -> FakeSigningKey:
        del token
        return FakeSigningKey(
            self._public_key
        )


def create_authenticator():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    config = AuthenticationConfig(
        mode="oidc",
        issuer=(
            "https://issuer.example/oauth2/default"
        ),
        audience="api://aletheus",
        jwks_url=(
            "https://issuer.example/oauth2/default/v1/keys"
        ),
        roles_claim="groups",
        entitlements_claim="scp",
    )

    authenticator = (
        OIDCPrincipalAuthenticator(config)
    )

    authenticator._jwk_client = (
        FakeJWKClient(
            private_key.public_key()
        )
    )

    return authenticator, private_key


def test_oidc_authenticator_maps_valid_claims() -> None:
    from datetime import (
        UTC,
        datetime,
        timedelta,
    )

    authenticator, private_key = (
        create_authenticator()
    )

    now = datetime.now(UTC)

    token = jwt.encode(
        {
            "sub": "user-1",
            "name": "User One",
            "iss": (
                "https://issuer.example/oauth2/default"
            ),
            "aud": "api://aletheus",
            "iat": now,
            "exp": now + timedelta(minutes=5),
            "groups": [
                "operator",
                "unrelated-group",
            ],
            "scp": [
                "runtime.read",
                "providers.refresh",
            ],
        },
        private_key,
        algorithm="RS256",
    )

    principal = authenticator.authenticate(
        token
    )

    assert principal.subject_id == "user-1"
    assert principal.roles == ("operator",)
    assert "runtime.read" in (
        principal.entitlements
    )


def test_oidc_authenticator_rejects_wrong_audience() -> None:
    from datetime import (
        UTC,
        datetime,
        timedelta,
    )

    authenticator, private_key = (
        create_authenticator()
    )

    now = datetime.now(UTC)

    token = jwt.encode(
        {
            "sub": "user-1",
            "iss": (
                "https://issuer.example/oauth2/default"
            ),
            "aud": "api://wrong",
            "iat": now,
            "exp": now + timedelta(minutes=5),
        },
        private_key,
        algorithm="RS256",
    )

    with pytest.raises(
        AuthenticationFailure,
        match="audience",
    ):
        authenticator.authenticate(token)
