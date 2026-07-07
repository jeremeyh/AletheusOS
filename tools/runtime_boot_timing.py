from time import sleep

from aletheus.runtime.boot_pipeline.manifest import BOOT_PHASES
from aletheus.runtime.boot_pipeline.timing import BootTiming


def main():

    print("========================================================")
    print("ALETHEUSOS RUNTIME BOOT TIMING")
    print("========================================================")
    print()

    total = 0.0

    for phase in BOOT_PHASES:

        timer = BootTiming(phase)

        #
        # Placeholder until the boot pipeline records
        # actual phase execution times.
        #
        sleep(0.001)

        timer.stop()

        total += timer.milliseconds

        print(f"{phase:.<45}{timer.milliseconds:7.2f} ms")

    print()
    print(f"Total Boot Time.................{total:.2f} ms")
    print("========================================================")


if __name__ == "__main__":
    main()
