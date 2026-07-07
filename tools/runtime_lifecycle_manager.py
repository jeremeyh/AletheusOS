from aletheus.runtime.lifecycle import (
    RuntimeLifecycleManager,
)


def main():

    lifecycle = RuntimeLifecycleManager()

    print("========================================================")
    print("ALETHEUSOS LIFECYCLE MANAGER")
    print("========================================================")
    print()

    print(lifecycle.state.value)

    lifecycle.initialize()
    print(lifecycle.state.value)

    lifecycle.boot()
    print(lifecycle.state.value)

    lifecycle.online()
    print(lifecycle.state.value)

    lifecycle.degrade()
    print(lifecycle.state.value)

    lifecycle.recover()
    print(lifecycle.state.value)

    lifecycle.shutdown()
    print(lifecycle.state.value)

    lifecycle.offline()
    print(lifecycle.state.value)

    print()
    print("========================================================")


if __name__ == "__main__":
    main()
