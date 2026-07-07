from aletheus.runtime.decomposition import (
    RuntimeCoreDecompositionPlanner,
    RuntimeCoreDecompositionReporter,
)


def main():
    plan = RuntimeCoreDecompositionPlanner().plan()
    print(RuntimeCoreDecompositionReporter().render(plan))


if __name__ == "__main__":
    main()
