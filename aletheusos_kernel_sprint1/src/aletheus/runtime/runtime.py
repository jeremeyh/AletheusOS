from aletheus.core import VERSION, Event, LifecycleState, Result
from aletheus.kernel import ConstitutionalKernel
from aletheus.sdk.mission import MissionContext


class AletheusRuntime:
    def __init__(self,kernel=None): self.kernel=kernel or ConstitutionalKernel()
    def boot(self):
        self.kernel.transition(LifecycleState.GENESIS); self.kernel.constitution.validate()
        self.kernel.transition(LifecycleState.BOOTSTRAP); self.kernel.services.register("event_bus",self.kernel.events); self.kernel.services.register("memory",self.kernel.memory)
        self.kernel.transition(LifecycleState.COMPOSE); self.kernel.events.publish(Event("constitution.loaded","runtime",{"version":self.kernel.constitution.version}))
        self.kernel.transition(LifecycleState.OPERATIONAL)
    def register_mission(self,mission):
        self.kernel.missions.register(mission.key,mission); self.kernel.events.publish(Event("mission.registered","runtime",{"key":mission.key}))
    def execute_mission(self,key):
        if self.kernel.lifecycle is not LifecycleState.OPERATIONAL: return Result.fail("Runtime is not operational.")
        mission=self.kernel.missions.get(key); cid=mission.new_correlation_id(); return mission.execute(MissionContext(self.kernel.events,self.kernel.memory,cid))
    def stop(self):
        self.kernel.transition(LifecycleState.STEWARDSHIP); self.kernel.events.publish(Event("runtime.stewardship.completed","runtime",{"learning_records":len(self.kernel.memory.records)})); self.kernel.transition(LifecycleState.REST)
    def print_status(self,result):
        line="═"*42
        print(line); print("AletheusOS™"); print(f"Version: {VERSION}"); print(f"Constitution: {self.kernel.constitution.version}"); print(f"Lifecycle: {self.kernel.lifecycle.value.title()}"); print(f"Health: {self.kernel.health.value.title()}"); print(f"Registered Services: {self.kernel.services.count()}"); print(f"Registered Missions: {self.kernel.missions.count()}"); print(f"Events Emitted: {len(self.kernel.events.history)}"); print(f"Learning Records: {len(self.kernel.memory.records)}"); print(f"Mission Result: {result.message}"); print(line)
