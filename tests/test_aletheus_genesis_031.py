from aletheus.runtime import runtime_core, RuntimeContext, Pipeline, WorkflowGraph


def sample_engine(context: RuntimeContext) -> RuntimeContext:
    context.add_result("sample_engine", {"status": "ok"})
    return context


def test_runtime_health():
    context = runtime_core.commands.dispatch("runtime.health")
    assert not context.errors
    assert context.results["health"]["status"] == "online"


def test_runtime_diagnostics():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    assert not context.errors
    assert "diagnostics" in context.results


def test_pipeline_execution():
    runtime_core.register_engine("Sample Engine", sample_engine)

    pipeline = Pipeline("Sample Pipeline")
    pipeline.add_step("Sample Step", "Sample Engine")
    runtime_core.register_pipeline(pipeline)

    context = RuntimeContext(command="pipeline.test")
    result = runtime_core.pipelines.execute("Sample Pipeline", context)

    assert not result.errors
    assert "sample_engine" in result.results


def test_job_queue():
    job = runtime_core.queue.enqueue("runtime.health", {})
    completed = runtime_core.queue.run_next()

    assert completed is not None
    assert completed.job_id == job.job_id
    assert completed.status == "completed"


def test_workflow_execution():
    workflow = WorkflowGraph("Runtime Health Workflow")
    workflow.add_node("health", "runtime.health", {})
    runtime_core.register_workflow(workflow)

    result = runtime_core.workflows.execute("Runtime Health Workflow")

    assert not result.errors
    assert "workflow" in result.results


if __name__ == "__main__":
    test_runtime_health()
    test_runtime_diagnostics()
    test_pipeline_execution()
    test_job_queue()
    test_workflow_execution()
    print("Aletheus Genesis 0.3.1 Runtime Consolidation tests passed.")
