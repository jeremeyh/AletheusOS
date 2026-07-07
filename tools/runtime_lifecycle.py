from aletheus.runtime.lifecycle import RuntimeLifecycleState


def main():

    print("========================================================")
    print("ALETHEUSOS RUNTIME LIFECYCLE")
    print("========================================================")
    print()

    for state in RuntimeLifecycleState:
        print(state.value)

    print()
    print("States.........................", len(RuntimeLifecycleState))
    print("========================================================")


if __name__ == "__main__":
    main()
