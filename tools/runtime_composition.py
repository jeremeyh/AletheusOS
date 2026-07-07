from aletheus.runtime.composition import (
    RuntimeCompositionRoot,
    RuntimeCompositionReporter,
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
