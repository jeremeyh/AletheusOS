from aletheus.platform_intelligence.runtime_snapshot import (
    RuntimeSnapshotService,
)


class DemoDiagnostics:
    def report(self):
        return {
            "status": "healthy"
        }


class DemoComponent:

    def __init__(self, name):
        self.name = name

    def stats(self):
        return {
            "component": self.name,
            "status": "online",
        }


class DemoRuntime:

    diagnostics = DemoDiagnostics()

    memory = DemoComponent("memory")
    cognition = DemoComponent("cognition")
    knowledge = DemoComponent("knowledge")
    mission = DemoComponent("mission")
    workspace = DemoComponent("workspace")
    applications = DemoComponent("applications")
    semantic = DemoComponent("semantic")
    executive = DemoComponent("executive")
    agents = DemoComponent("agents")
    planning = DemoComponent("planning")
    copilot = DemoComponent("copilot")
    intelligence = DemoComponent("uil")
    prediction = DemoComponent("prediction")
    learning = DemoComponent("learning")
    kernel_v2 = DemoComponent("kernel_v2")
    mission_v2 = DemoComponent("mission_v2")
    workflow_v2 = DemoComponent("workflow_v2")
    enterprise = DemoComponent("enterprise")
    distributed = DemoComponent("distributed")
    memory_mesh = DemoComponent("memory_mesh")
    knowledge_graph = DemoComponent("knowledge_graph")


def main():

    runtime = DemoRuntime()

    snapshot = RuntimeSnapshotService().collect(runtime)

    print("========================================================")
    print("ALETHEUSOS RUNTIME SNAPSHOT")
    print("========================================================")
    print()

    for key in sorted(snapshot.keys()):
        print(f"{key}")

    print()
    print(f"Components: {len(snapshot)}")
    print("========================================================")


if __name__ == "__main__":
    main()
