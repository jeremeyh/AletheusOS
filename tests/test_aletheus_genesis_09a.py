from aletheus.runtime import runtime_core


def test_application_manager_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Native Application Manager" in diagnostics["services"]


def test_cardhawk_registered():
    context = runtime_core.commands.dispatch("application.list", {})
    applications = context.results["applications"]
    names = [app["name"] for app in applications]
    assert "Card Hawk Foundation™" in names


def test_cardhawk_start_and_status():
    started = runtime_core.commands.dispatch("cardhawk.start", {})
    assert not started.errors
    assert started.results["cardhawk"]["status"] == "running"

    status = runtime_core.commands.dispatch("cardhawk.status", {})
    assert not status.errors
    assert status.results["cardhawk"]["health"] == "healthy"


def test_application_stats():
    stats = runtime_core.commands.dispatch("application.stats", {})
    assert not stats.errors
    assert stats.results["application_stats"]["applications"] >= 1


if __name__ == "__main__":
    test_application_manager_registered()
    test_cardhawk_registered()
    test_cardhawk_start_and_status()
    test_application_stats()
    print("Aletheus Genesis 0.9A Native Application Manager tests passed.")
