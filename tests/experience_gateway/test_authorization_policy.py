from __future__ import annotations

from aletheus.experience_gateway.security.contracts import (
    Principal,
)
from aletheus.experience_gateway.security.default_policy import (
    create_default_authorization_policy,
)


def test_viewer_can_run_entitled_read_only_command() -> None:
    policy = create_default_authorization_policy()

    decision = policy.evaluate(
        principal=Principal(
            subject_id="viewer-1",
            display_name="Viewer",
            roles=("viewer",),
            entitlements=("runtime.read",),
        ),
        command_id="runtime.describe",
        command_risk="read_only",
        required_entitlements=("runtime.read",),
    )

    assert decision.allowed is True


def test_viewer_cannot_run_low_risk_write_command() -> None:
    policy = create_default_authorization_policy()

    decision = policy.evaluate(
        principal=Principal(
            subject_id="viewer-1",
            display_name="Viewer",
            roles=("viewer",),
            entitlements=("experience.preferences.write",),
        ),
        command_id="experience.inspector.set",
        command_risk="low",
        required_entitlements=("experience.preferences.write",),
    )

    assert decision.allowed is False
    assert "operator" in decision.reason


def test_missing_entitlement_is_denied() -> None:
    policy = create_default_authorization_policy()

    decision = policy.evaluate(
        principal=Principal(
            subject_id="operator-1",
            display_name="Operator",
            roles=("operator",),
            entitlements=(),
        ),
        command_id="providers.refresh",
        command_risk="read_only",
        required_entitlements=("providers.refresh",),
    )

    assert decision.allowed is False
    assert "providers.refresh" in decision.reason


def test_platform_architect_can_run_high_risk_command() -> None:
    policy = create_default_authorization_policy()

    decision = policy.evaluate(
        principal=Principal(
            subject_id="architect-1",
            display_name="Architect",
            roles=("platform_architect",),
            entitlements=("platform.control",),
        ),
        command_id="platform.control",
        command_risk="high",
        required_entitlements=("platform.control",),
    )

    assert decision.allowed is True
