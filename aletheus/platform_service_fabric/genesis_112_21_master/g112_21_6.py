from __future__ import annotations
from typing import Dict
from .common import *

class RuntimeBindingCoordinator:
    """Coordinates activation; it is not a registry and owns no service authority."""
    def __init__(self, topology_digest:str=PREDECESSOR_TOPOLOGY_DIGEST):
        if topology_digest != PREDECESSOR_TOPOLOGY_DIGEST:
            raise RuntimeError("stale or foreign topology digest refused")
        self._states: Dict[str,ActivationState]={}
        self._owners: Dict[str,str]={}

    def bind(self, intent:BindingIntent) -> BindingReceipt:
        if intent.topology_digest != PREDECESSOR_TOPOLOGY_DIGEST:
            return self._r(intent.service_id,ActivationState.FAILED,False,"topology digest mismatch")
        if not intent.service_id or not intent.owner:
            return self._r(intent.service_id,ActivationState.FAILED,False,"missing service identity/owner")
        if intent.service_id in self._owners:
            prior_owner=self._owners[intent.service_id]
            if prior_owner != intent.owner:
                return self._r(intent.service_id,ActivationState.FAILED,False,"conflicting owner")
            return self._r(intent.service_id,self._states[intent.service_id],False,"duplicate/replay binding refused")
        unresolved=[d for d in intent.dependencies if self._states.get(d) != ActivationState.ACTIVE]
        if unresolved:
            return self._r(intent.service_id,ActivationState.FAILED,False,"dependency inactive: "+",".join(sorted(unresolved)))
        self._owners[intent.service_id]=intent.owner
        self._states[intent.service_id]=ActivationState.BOUND
        return self._r(intent.service_id,ActivationState.BOUND,True,"bounded binding accepted")

    def activate(self, service_id:str) -> BindingReceipt:
        if self._states.get(service_id) != ActivationState.BOUND:
            return self._r(service_id,ActivationState.FAILED,False,"service not in BOUND state")
        self._states[service_id]=ActivationState.ACTIVE
        return self._r(service_id,ActivationState.ACTIVE,True,"activation accepted")

    def degrade(self, service_id:str, reason:str) -> BindingReceipt:
        if service_id not in self._states:
            return self._r(service_id,ActivationState.FAILED,False,"unknown service")
        self._states[service_id]=ActivationState.DEGRADED
        return self._r(service_id,ActivationState.DEGRADED,True,reason)

    def rollback(self, service_id:str) -> BindingReceipt:
        if service_id not in self._states:
            return self._r(service_id,ActivationState.FAILED,False,"unknown service")
        self._states[service_id]=ActivationState.ROLLED_BACK
        return self._r(service_id,ActivationState.ROLLED_BACK,True,"binding rolled back")

    def state(self, service_id:str):
        return self._states.get(service_id)

    def _r(self,s,state,ok,reason):
        return BindingReceipt(s,state,ok,reason,digest({"service":s,"state":state.value,"accepted":ok,"reason":reason}))

class MammothAssurancePort:
    """Only accepted durable evidence path."""
    def __init__(self, gateway):
        if gateway is None or not callable(getattr(gateway,"persist_assurance_evidence",None)):
            raise RuntimeError("certified Mammoth gateway required")
        self.gateway=gateway
    def persist(self, payload):
        return self.gateway.persist_assurance_evidence(payload)

class RSFReliabilityPort:
    """RSF retains reliability authority; service fabric only consumes observations."""
    def __init__(self, observer):
        if observer is None or not callable(getattr(observer,"observe",None)):
            raise RuntimeError("RSF observer required")
        self.observer=observer
    def observe(self, service_id:str):
        return self.observer.observe(service_id)
