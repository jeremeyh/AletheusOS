from aletheus.runtime.core_bridge import (
    CoreLifecycleBridge,
    CoreLifecycleBridgeReporter,
)


def main():

    bridge = CoreLifecycleBridge()

    report = bridge.boot()

    print(
        CoreLifecycleBridgeReporter().render(
            report
        )
    )


if __name__ == "__main__":
    main()
