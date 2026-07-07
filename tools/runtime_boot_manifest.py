from aletheus.runtime.boot_pipeline.manifest import BOOT_PHASES


def main():
    print("========================================================")
    print("ALETHEUSOS RUNTIME BOOT MANIFEST")
    print("========================================================")
    print()

    for index, phase in enumerate(BOOT_PHASES, start=1):
        print(f"{index}. {phase}")

    print()
    print(f"Boot Phases....................{len(BOOT_PHASES)}")
    print("========================================================")


if __name__ == "__main__":
    main()
