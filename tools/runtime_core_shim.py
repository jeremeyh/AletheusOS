from aletheus.runtime.core_shim import (
    RuntimeCoreShim,
    RuntimeCoreShimReporter,
)


def main():

    shim = RuntimeCoreShim()

    report = shim.bootstrap()

    print(
        RuntimeCoreShimReporter().render(
            report
        )
    )


if __name__ == "__main__":
    main()
