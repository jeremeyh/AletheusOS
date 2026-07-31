from aletheus.core import LifecycleState
from aletheus.sdk.hello_mission import HelloMission

from aletheus.runtime import AletheusRuntime


def test_runtime_vertical_slice():
    runtime = AletheusRuntime()
    runtime.boot()
    runtime.register_mission(HelloMission())
    result = runtime.execute_mission("hello.mission")
    assert runtime.kernel.lifecycle is LifecycleState.OPERATIONAL
    assert result.success and result.value["status"] == "success"
    assert len(runtime.kernel.memory.records) == 1
    runtime.stop()
    assert runtime.kernel.lifecycle is LifecycleState.REST
