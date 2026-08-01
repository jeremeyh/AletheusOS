import json

from aletheus.tooling.execution_runtime.engine import ExecutionRuntime


def test_runtime_executes_real_steps(tmp_path) -> None:
    grid = tmp_path / "grid.json"
    grid.write_text(
        json.dumps(
            {
                "steps": [
                    {"step_id": "1", "stage": "Evidence Validation"},
                    {"step_id": "2", "stage": "Platform Certification"},
                ]
            }
        )
    )
    runtime = ExecutionRuntime(grid, tmp_path / "out")
    result = runtime.execute_sync("mission-1")
    assert result.status == "completed"
    assert len(result.steps) == 2
