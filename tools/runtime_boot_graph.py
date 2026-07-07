from aletheus.runtime.boot_pipeline.dependencies import BOOT_DEPENDENCIES


def main():

    print("========================================================")
    print("ALETHEUSOS RUNTIME BOOT GRAPH")
    print("========================================================")
    print()

    for phase, deps in BOOT_DEPENDENCIES.items():

        if deps:
            print(f"{phase}")
            for dep in deps:
                print(f"   └── depends on {dep}")
        else:
            print(f"{phase}")
            print("   └── root phase")

        print()

    print("Boot Phases....................", len(BOOT_DEPENDENCIES))
    print("========================================================")


if __name__ == "__main__":
    main()
