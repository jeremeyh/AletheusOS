from aletheus.platform.contracts import PlatformService


class DemoService(PlatformService):
    pass


def main():

    service = DemoService()

    print("========================================================")
    print("ALETHEUSOS PLATFORM SERVICE CONTRACT")
    print("========================================================")
    print()

    print(service.health())
    print(service.metrics())
    print(service.snapshot())

    print()
    print("Status....................PASS")
    print("========================================================")


if __name__ == "__main__":
    main()
