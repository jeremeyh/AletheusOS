from aletheus.runtime import runtime_core


def test_application_framework_online():
    result = runtime_core.commands.dispatch("application.stats", {})
    assert not result.errors, result.errors
    print(result.results)


def test_bootstrap_default_native_apps():
    result = runtime_core.commands.dispatch("application.bootstrap.defaults", {})
    assert not result.errors, result.errors

    print("\nBOOTSTRAP")
    print(result.results)


def test_application_manifest():
    result = runtime_core.commands.dispatch(
        "application.manifest",
        {"app_id": "cardhawk.foundation"},
    )

    print("\nMANIFEST")
    print(result.results)


def test_application_lifecycle():

    runtime_core.commands.dispatch(
        "application.bootstrap.defaults",
        {},
    )

    stopped = runtime_core.commands.dispatch(
        "application.stop",
        {"app_id": "cardhawk.foundation"},
    )

    print("\nERRORS")
    print(stopped.errors)

    print("\nRESULTS")
    print(stopped.results)

    started = runtime_core.commands.dispatch(
        "application.start",
        {"app_id": "cardhawk.foundation"},
    )

    print("\nSTART RESULTS")
    print(started.results)


if __name__ == "__main__":
    test_application_framework_online()
    test_bootstrap_default_native_apps()
    test_application_manifest()
    test_application_lifecycle()
