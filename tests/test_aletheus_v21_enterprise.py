from aletheus.runtime import runtime_core


def test_enterprise_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Enterprise Intelligence Platform" in diagnostics["services"]


def test_bootstrap_cardhawk_enterprise():
    result = runtime_core.commands.dispatch("enterprise.bootstrap.cardhawk", {})
    assert not result.errors, result.errors
    assert "enterprise" in result.results
    assert result.results["enterprise"]["name"] == "Card Hawk Enterprise™"
    assert len(result.results["enterprise"]["departments"]) >= 1
    assert len(result.results["enterprise"]["policies"]) >= 1


def test_create_enterprise_department_team_policy():
    created = runtime_core.commands.dispatch(
        "enterprise.create",
        {
            "name": "6th Dimension Multimedia Enterprise",
            "description": "Parent enterprise for AletheusOS native operations.",
            "applications": ["AletheusOS", "Card Hawk Foundation™"],
        },
    )
    org = created.results["enterprise"]

    department = runtime_core.commands.dispatch(
        "department.create",
        {
            "organization_id": org["organization_id"],
            "name": "Platform Engineering",
            "description": "Builds AletheusOS.",
        },
    )
    assert not department.errors, department.errors
    dept = department.results["department"]

    team = runtime_core.commands.dispatch(
        "team.create",
        {
            "organization_id": org["organization_id"],
            "department_id": dept["department_id"],
            "name": "Kernel Team",
            "members": ["Founder"],
        },
    )
    assert not team.errors, team.errors

    policy = runtime_core.commands.dispatch(
        "policy.create",
        {
            "organization_id": org["organization_id"],
            "name": "Execution Governance",
            "description": "Founder approval required for critical execution.",
            "rules": ["require_founder_approval_for_external_api_actions"],
        },
    )
    assert not policy.errors, policy.errors


def test_governance_and_audit():
    bootstrap = runtime_core.commands.dispatch("enterprise.bootstrap.cardhawk", {})
    org = bootstrap.results["enterprise"]

    check = runtime_core.commands.dispatch(
        "governance.check",
        {
            "organization_id": org["organization_id"],
            "actor": "founder",
            "action": "execute external marketplace purchase",
            "target": "Card Hawk Foundation™",
        },
    )
    assert not check.errors, check.errors
    assert "governance" in check.results
    assert check.results["governance"]["outcome"] in {"approved", "requires_founder_review"}

    audit = runtime_core.commands.dispatch("audit.history", {})
    assert not audit.errors, audit.errors
    assert "audit" in audit.results
    assert len(audit.results["audit"]) >= 1


def test_enterprise_stats():
    result = runtime_core.commands.dispatch("enterprise.stats", {})
    assert not result.errors, result.errors
    assert "enterprise_stats" in result.results


if __name__ == "__main__":
    test_enterprise_service_registered()
    test_bootstrap_cardhawk_enterprise()
    test_create_enterprise_department_team_policy()
    test_governance_and_audit()
    test_enterprise_stats()
    print("Aletheus v2.1 Enterprise Intelligence Platform tests passed.")
