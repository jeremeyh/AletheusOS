from aletheus.sdk.hello_mission import HelloMission

from aletheus.runtime import AletheusRuntime


def main():
    runtime = AletheusRuntime()
    runtime.boot()
    runtime.register_mission(HelloMission())
    result = runtime.execute_mission("hello.mission")
    runtime.print_status(result)
    runtime.stop()


if __name__ == "__main__":
    main()
