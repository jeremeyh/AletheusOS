from __future__ import annotations

from aletheus.platform_intelligence import (
    ConstitutionalPolicyEngine,
    ConstitutionalRuntimeExecutive,
    ConstitutionalRuntimeKernel,
    ConstitutionalRuntimeSupervisor,
    ExecutiveDecision,
    default_executive_policies,
)


def build_executive():
    kernel = ConstitutionalRuntimeKernel()

    supervisor = ConstitutionalRuntimeSupervisor(kernel=kernel)

    supervisor.start_platform()

    policy_engine = ConstitutionalPolicyEngine(
        default_executive_policies(),
        freeze=True,
    )

    executive = ConstitutionalRuntimeExecutive(
        kernel=kernel,
        supervisor=supervisor,
        policy_engine=policy_engine,
    )

    return policy_engine, executive


def test_crx_uses_injected_policy_engine() -> None:
    policy_engine, executive = build_executive()

    assert executive.policy_engine is policy_engine


def test_crx_behavior_is_preserved() -> None:
    policy_engine, executive = build_executive()

    recommendation = executive.evaluate()

    assert recommendation.decision is (ExecutiveDecision.NO_ACTION)

    assert policy_engine.statistics().evaluations == 1


def test_crx_export_contains_policy_snapshot() -> None:
    _, executive = build_executive()

    executive.evaluate()
    payload = executive.export()

    assert "policy_engine" in payload
    assert payload["policy_engine"]["version"] == "9.16.0"


def test_crx_does_not_own_policy_registry() -> None:
    _, executive = build_executive()

    forbidden = {
        "register_policy",
        "remove_policy",
        "freeze_policies",
    }

    assert forbidden.isdisjoint(set(dir(executive)))
