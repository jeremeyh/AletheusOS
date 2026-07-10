from __future__ import annotations

import pytest
from fastapi import HTTPException

from aletheus.experience_gateway.security.contracts import (
    Principal,
)
from aletheus.experience_gateway.security.oidc_authenticator import (
    AuthenticationFailure,
)
from aletheus.experience_gateway.security.resolver import (
    PrincipalResolver,
)


class SuccessfulAuthenticator:
    def authenticate(
        self,
        credential: str | None,
    ) -> Principal:
        assert credential == "token-value"

        return Principal(
            subject_id="user-1",
            display_name="User One",
            roles=("operator",),
            entitlements=("runtime.read",),
            authentication_method="test",
        )


class FailingAuthenticator:
    def authenticate(
        self,
        credential: str | None,
    ) -> Principal:
        del credential

        raise AuthenticationFailure(
            "Token is invalid."
        )


def test_resolver_accepts_bearer_token() -> None:
    resolver = PrincipalResolver(
        SuccessfulAuthenticator()
    )

    principal = resolver.dependency(
        authorization=(
            "Bearer token-value"
        )
    )

    assert principal.subject_id == "user-1"


def test_resolver_rejects_invalid_scheme() -> None:
    resolver = PrincipalResolver(
        SuccessfulAuthenticator()
    )

    with pytest.raises(HTTPException) as error:
        resolver.dependency(
            authorization="Basic token-value"
        )

    assert error.value.status_code == 401


def test_resolver_maps_auth_failure_to_401() -> None:
    resolver = PrincipalResolver(
        FailingAuthenticator()
    )

    with pytest.raises(HTTPException) as error:
        resolver.dependency(
            authorization="Bearer bad-token"
        )

    assert error.value.status_code == 401
