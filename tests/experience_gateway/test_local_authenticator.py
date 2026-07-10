from __future__ import annotations

from aletheus.experience_gateway.security.local_authenticator import (
    LocalPrincipalAuthenticator,
)


def test_local_authenticator_returns_environment_principal(
    monkeypatch,
) -> None:
    monkeypatch.setenv(
        "ALETHEUS_LOCAL_SUBJECT",
        "local:test-user",
    )

    monkeypatch.setenv(
        "ALETHEUS_LOCAL_DISPLAY_NAME",
        "Test User",
    )

    monkeypatch.setenv(
        "ALETHEUS_LOCAL_ROLES",
        "operator",
    )

    monkeypatch.setenv(
        "ALETHEUS_LOCAL_ENTITLEMENTS",
        "runtime.read,providers.refresh",
    )

    principal = (
        LocalPrincipalAuthenticator()
        .authenticate(None)
    )

    assert principal.subject_id == (
        "local:test-user"
    )

    assert principal.roles == (
        "operator",
    )

    assert "runtime.read" in (
        principal.entitlements
    )
