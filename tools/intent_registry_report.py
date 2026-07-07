from aletheus.intent_registry import bootstrap_intents, IntentRegistryReporter


def main():
    registry = bootstrap_intents()
    print(IntentRegistryReporter().render(registry))


if __name__ == "__main__":
    main()
