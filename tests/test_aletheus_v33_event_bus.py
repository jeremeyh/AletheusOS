from aletheus.runtime import runtime_core


def test_event_service_registered():

    ctx = runtime_core.commands.dispatch("runtime.diagnostics")

    diagnostics = ctx.results["diagnostics"]

    assert "Aletheus Event Bus" in diagnostics["services"]


def test_bootstrap():

    result = runtime_core.commands.dispatch(
        "event.bootstrap",
        {},
    )

    assert not result.errors, result.errors

    stats = result.results["event_bus"]

    assert stats["health"] == "healthy"


def test_publish():

    result = runtime_core.commands.dispatch(

        "event.publish",

        {
            "topic": "runtime.test",

            "publisher": "unit-test",

            "payload": {
                "message": "hello"
            },

            "priority": "normal",
        },
    )

    assert not result.errors

    event = result.results["event"]

    assert event["topic"] == "runtime.test"

    assert event["publisher"] == "unit-test"


def test_subscribe():

    result = runtime_core.commands.dispatch(

        "event.subscribe",

        {
            "topic": "runtime.test",

            "subscriber": "Workflow Engine",
        },
    )

    assert not result.errors

    sub = result.results["subscription"]

    assert sub["subscriber_count"] >= 1


def test_history():

    result = runtime_core.commands.dispatch(

        "event.history",

        {
            "topic": "runtime.test"
        },
    )

    assert not result.errors

    assert isinstance(result.results["history"], list)


def test_replay():

    result = runtime_core.commands.dispatch(

        "event.replay",

        {
            "topic": "runtime.test"
        },
    )

    assert not result.errors

    replay = result.results["replay"]

    assert replay["topic"] == "runtime.test"


def test_unsubscribe():

    result = runtime_core.commands.dispatch(

        "event.unsubscribe",

        {
            "topic": "runtime.test",

            "subscriber": "Workflow Engine",
        },
    )

    assert not result.errors


def test_statistics():

    result = runtime_core.commands.dispatch(

        "event.statistics",

        {},
    )

    assert not result.errors

    stats = result.results["event_stats"]

    assert stats["health"] == "healthy"


if __name__ == "__main__":

    test_event_service_registered()

    test_bootstrap()

    test_publish()

    test_subscribe()

    test_history()

    test_replay()

    test_unsubscribe()

    test_statistics()

    print("\n✔ AletheusOS v3.3 Event Bus tests passed.")
