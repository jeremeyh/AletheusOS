from aletheus.runtime.composition import (
    RuntimeCompositionReporter,
    RuntimeCompositionRoot,
)


def main():

    root = RuntimeCompositionRoot()

    runtime = root.build()

    print(
        RuntimeCompositionReporter().render(
            runtime
        )
    )


if __name__ == "__main__":
    main()
