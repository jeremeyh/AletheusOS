from aletheus.runtime import runtime_core


def test_release_status():
    result = runtime_core.commands.dispatch("release.status", {})
    assert not result.errors
    assert result.results["release"]["version"] == "1.0.0-genesis"


def test_release_validation():
    result = runtime_core.commands.dispatch("release.validate", {})
    assert not result.errors
    validation = result.results["validation"]
    assert validation["runtime_health"]["status"] == "online"
    assert validation["stable"] is True


def test_cardhawk_reference_application_present():
    result = runtime_core.commands.dispatch("application.list", {})
    names = [app["name"] for app in result.results["applications"]]
    assert "Card Hawk Foundation™" in names


if __name__ == "__main__":
    test_release_status()
    test_release_validation()
    test_cardhawk_reference_application_present()
    print("Aletheus Genesis 1.0 Core Stable tests passed.")
