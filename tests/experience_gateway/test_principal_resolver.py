from __future__ import annotations

import pytest
from fastapi import HTTPException

from aletheus.experience_gateway.security.resolver import (
    PrincipalResolver,
)


def test_resolver_uses_trusted_headers() -> None:
    resolver = PrincipalResolver()

    principal = resolver.resolve(
        subject="user-1",
        display_name="User One",
        roles_header="operator,viewer",
        entitlements_header=(
            "runtime.read,providers.refresh"
        ),
    )

    assert principal.subject_id == "user-1"
    assert "operator" in principal.roles
    assert "providers.refresh" in (
        principal.entitlements
    )


def test_resolver_rejects_invalid_role() -> None:
    resolver = PrincipalResolver()

    with pytest.raises(HTTPException):
        resolver.resolve(
            subject="user-1",
            display_name="User One",
            roles_header="superuser",
            entitlements_header=None,
        )


def test_resolver_can_require_authentication() -> None:
    resolver = PrincipalResolver(
        allow_local_identity=False
    )

    with pytest.raises(HTTPException) as error:
        resolver.resolve(
            subject=None,
            display_name=None,
            roles_header=None,
            entitlements_header=None,
        )

    assert error.value.status_code == 401
