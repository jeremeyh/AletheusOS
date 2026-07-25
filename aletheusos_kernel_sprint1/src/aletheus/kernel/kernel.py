from aletheus.constitution import Constitution
from aletheus.core import Event, HealthStatus, LifecycleState

from .event_bus import EventBus
from .memory import InMemoryLearningStore
from .registry import Registry


class ConstitutionalKernel:
    def __init__(self,constitution=None):
        self.constitution=constitution or Constitution(); self.events=EventBus(); self.services=Registry(); self.missions=Registry(); self.memory=InMemoryLearningStore(); self.lifecycle=LifecycleState.DORMANT; self.health=HealthStatus.HEALTHY
    def transition(self,target):
        previous=self.lifecycle; self.lifecycle=target
        self.events.publish(Event("runtime.lifecycle.changed","constitutional_kernel",{"from":previous.value,"to":target.value}))
