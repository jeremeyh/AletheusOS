from aletheus.runtime.executive import ExecutiveKernel, ExecutiveKernelReporter


def main():
    kernel = ExecutiveKernel()

    kernel.activate_service("Runtime Registry")
    kernel.activate_service("Capability Registry")
    kernel.activate_service("Relay Network")
    kernel.activate_service("Catalyst")
    kernel.register_mission("Reduce runtime core responsibility")

    print(ExecutiveKernelReporter().render(kernel))


if __name__ == "__main__":
    main()
