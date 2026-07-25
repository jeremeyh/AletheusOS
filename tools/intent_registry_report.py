from aletheus.intent_registry import IntentRegistryReporter, bootstrap_intents


def main():
    registry = bootstrap_intents()
    print(IntentRegistryReporter().render(registry))


if __name__ == "__main__":
    main()
