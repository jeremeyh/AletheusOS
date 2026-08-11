from __future__ import annotations
from .common import *
from .g112_21_6 import RuntimeBindingCoordinator

class RuntimeLifecycleReliabilityIntegrator:
    def __init__(self, binding:RuntimeBindingCoordinator):
        self.binding=binding

    def reconcile(self, service_id:str, lifecycle_state:str, health_state:str, rsf_state:str) -> ReliabilityObservation:
        if self.binding.state(service_id) is None:
            raise RuntimeError("observation refused for unbound service")
        normalized=rsf_state.upper()
        if normalized not in {"HEALTHY","DEGRADED","RECOVERING","FAULTED","OFFLINE"}:
            raise RuntimeError("unknown RSF reliability state")
        if normalized in {"FAULTED","OFFLINE"}:
            self.binding.degrade(service_id,f"RSF reliability state {normalized}")
        return ReliabilityObservation(
            service_id=service_id,
            lifecycle_state=lifecycle_state,
            health_state=health_state,
            reliability_state=normalized,
            evidence_digest=digest({
                "service":service_id,"lifecycle":lifecycle_state,
                "health":health_state,"reliability":normalized
            })
        )

    @staticmethod
    def activation_permitted(binding_authorized:bool, reliability_state:str) -> bool:
        return bool(binding_authorized and reliability_state.upper() in {"HEALTHY","RECOVERING"})

    @staticmethod
    def truths_are_distinct(binding_authorized:bool, health_state:str, reliability_state:str) -> dict:
        return {
            "bindingAuthorized":binding_authorized,
            "healthState":health_state,
            "reliabilityState":reliability_state,
            "bindingIsNotHealthProof":True,
            "healthIsNotAuthorizationProof":True,
        }
