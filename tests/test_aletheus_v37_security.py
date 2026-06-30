from aletheus.runtime import runtime_core


def test_security_service_registered():

    ctx = runtime_core.commands.dispatch("runtime.diagnostics")

    diagnostics = ctx.results["diagnostics"]

    assert "Aletheus Security & Policy Engine" in diagnostics["services"]


def test_bootstrap():

    result = runtime_core.commands.dispatch(
        "security.bootstrap",
        {},
    )

    assert not result.errors, result.errors

    stats = result.results["security"]

    assert stats["health"] == "healthy"


def test_create_role():

    result = runtime_core.commands.dispatch(

        "security.role.create",

        {
            "name": "Developer",
            "permissions": [
                "workflow.execute",
                "agent.spawn",
            ],
        },
    )

    assert not result.errors

    role = result.results["role"]

    assert role["name"] == "Developer"


def test_assign_role():

    result = runtime_core.commands.dispatch(

        "security.role.assign",

        {
            "identity": "jeremey",
            "role": "Developer",
        },
    )

    assert not result.errors

    assignment = result.results["assignment"]

    assert assignment["role"] == "Developer"


def test_authenticate():

    result = runtime_core.commands.dispatch(

        "security.authenticate",

        {
            "identity": "jeremey",
        },
    )

    assert not result.errors

    auth = result.results["authentication"]

    assert auth["authenticated"] is True


def test_authorize():

    result = runtime_core.commands.dispatch(

        "security.authorize",

        {
            "identity": "jeremey",
            "permission": "workflow.execute",
        },
    )

    assert not result.errors

    authorization = result.results["authorization"]

    assert authorization["authorized"] is True


def test_policy():

    result = runtime_core.commands.dispatch(

        "security.policy",

        {
            "name": "Default Runtime",
            "definition": {
                "allow_plugins": True,
            },
        },
    )

    assert not result.errors

    policy = result.results["policy"]

    assert policy["policy"] == "Default Runtime"


def test_audit():

    result = runtime_core.commands.dispatch(

        "security.audit",

        {
            "action": "workflow.execute",
            "actor": "jeremey",
        },
    )

    assert not result.errors

    audit = result.results["audit"]

    assert audit["actor"] == "jeremey"


def test_statistics():

    result = runtime_core.commands.dispatch(

        "security.statistics",

        {},
    )

    assert not result.errors

    stats = result.results["security_stats"]

    assert stats["health"] == "healthy"


if __name__ == "__main__":

    test_security_service_registered()
    test_bootstrap()
    test_create_role()
    test_assign_role()
    test_authenticate()
    test_authorize()
    test_policy()
    test_audit()
    test_statistics()

    print("\n✔ AletheusOS v3.7 Security & Policy Engine tests passed.")
