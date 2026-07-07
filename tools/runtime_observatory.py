from aletheus.platform_intelligence.runtime_observatory import (
    RuntimeObservatory,
)

from tools.runtime_snapshot import DemoRuntime


def main():

    runtime = DemoRuntime()

    observatory = RuntimeObservatory()

    overview = observatory.overview(runtime)

    print("========================================================")
    print("ALETHEUSOS RUNTIME OBSERVATORY")
    print("========================================================")
    print()

    print(f"Health Keys...............{len(overview['health'])}")
    print(f"Snapshot Components.......{len(overview['snapshot'])}")

    print()
    print("Status....................READY")
    print("========================================================")


if __name__ == "__main__":
    main()
