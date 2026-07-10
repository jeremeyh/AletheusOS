from aletheus.runtime import runtime_core


def test_service_registered():

    ctx = runtime_core.commands.dispatch("runtime.diagnostics")

    diagnostics = ctx.results["diagnostics"]

    assert "Aletheus Multi-Tenant Runtime" in diagnostics["services"]


def test_bootstrap():

    result = runtime_core.commands.dispatch(
        "tenant.bootstrap",
        {},
    )

    assert not result.errors

    stats = result.results["tenant"]

    assert stats["health"] == "healthy"

    assert stats["organizations"] >= 1

    assert stats["tenants"] >= 1


def test_create_organization():

    result = runtime_core.commands.dispatch(

        "organization.create",

        {
            "name": "Test Organization",
        },
    )

    assert not result.errors

    org = result.results["organization"]

    assert org["name"] == "Test Organization"

    assert org["organization_id"]


def test_create_tenant():

    org = runtime_core.tenancy_v3.create_organization(
        "Development Org"
    )

    result = runtime_core.commands.dispatch(

        "tenant.create",

        {
            "organization_id": org["organization_id"],
            "name": "Development",
        },
    )

    assert not result.errors

    tenant = result.results["tenant"]

    assert tenant["name"] == "Development"

    assert tenant["tenant_id"]


def test_workspace():

    tenant = runtime_core.tenancy_v3.create_tenant(

        organization_id=list(runtime_core.tenancy_v3.organizations.keys())[0],

        name="Workspace Tenant",

    )

    result = runtime_core.commands.dispatch(

        "workspace.create",

        {
            "tenant_id": tenant["tenant_id"],
            "name": "Engineering",
        },
    )

    assert not result.errors

    workspace = result.results["workspace"]

    assert workspace["name"] == "Engineering"


def test_statistics():

    result = runtime_core.commands.dispatch(
        "tenant.statistics",
        {},
    )

    assert not result.errors

    stats = result.results["tenant_stats"]

    assert stats["health"] == "healthy"


def test_health():

    result = runtime_core.commands.dispatch(
        "tenant.health",
        {},
    )

    assert not result.errors

    health = result.results["tenant_health"]

    assert health["health"] == "healthy"


if __name__ == "__main__":

    test_service_registered()

    test_bootstrap()

    test_create_organization()

    test_create_tenant()

    test_workspace()

    test_statistics()

    test_health()

    print("\n✔ AletheusOS v3.9 Multi-Tenant Runtime tests passed.")
