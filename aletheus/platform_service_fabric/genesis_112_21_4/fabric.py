from __future__ import annotations
import hashlib, json
from typing import Dict, Callable, Optional
from .contracts import *
from .mesh import ConnectionMesh

_ALLOWED = {
 LifecycleState.DISCOVERED:{LifecycleState.REGISTERED},
 LifecycleState.REGISTERED:{LifecycleState.INITIALIZING, LifecycleState.UNREGISTERED},
 LifecycleState.INITIALIZING:{LifecycleState.READY, LifecycleState.FAULTED},
 LifecycleState.READY:{LifecycleState.STARTING, LifecycleState.STOPPING},
 LifecycleState.STARTING:{LifecycleState.RUNNING, LifecycleState.FAULTED},
 LifecycleState.RUNNING:{LifecycleState.DEGRADED, LifecycleState.STOPPING, LifecycleState.FAULTED},
 LifecycleState.DEGRADED:{LifecycleState.RUNNING, LifecycleState.STOPPING, LifecycleState.FAULTED},
 LifecycleState.STOPPING:{LifecycleState.STOPPED, LifecycleState.FAULTED},
 LifecycleState.STOPPED:{LifecycleState.STARTING, LifecycleState.UNREGISTERED},
 LifecycleState.FAULTED:{LifecycleState.STOPPING},
 LifecycleState.UNREGISTERED:set(),
}

def _digest(obj) -> str:
    raw=json.dumps(obj, sort_keys=True, separators=(",",":"), default=str).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()

class RegistrationCoordinator:
    """Coordinates canonical registries; does not replace their authority."""
    def __init__(self, mesh: ConnectionMesh):
        self.mesh=mesh
        self.identities: Dict[str,ServiceIdentity]={}
        self.states: Dict[str,LifecycleState]={}

    def register(self, identity: ServiceIdentity) -> RegistrationReceipt:
        if not identity.service_id or not identity.owner or not identity.authority_domain:
            return self._receipt(identity.service_id, RegistrationDisposition.REFUSED, "missing identity/owner/authority")
        prior=self.identities.get(identity.service_id)
        if prior:
            if prior == identity:
                return self._receipt(identity.service_id, RegistrationDisposition.IDEMPOTENT, "identical registration already present")
            return self._receipt(identity.service_id, RegistrationDisposition.REFUSED, "conflicting service identity")
        missing=[d for d in identity.dependencies if d not in self.identities]
        if missing:
            return self._receipt(identity.service_id, RegistrationDisposition.REFUSED, "unresolved dependencies: "+",".join(sorted(missing)))
        self.identities[identity.service_id]=identity
        self.states[identity.service_id]=LifecycleState.REGISTERED
        for dep in identity.dependencies:
            self.mesh.connect(identity.service_id, dep, "DEPENDS_ON", identity.authority_domain)
        return self._receipt(identity.service_id, RegistrationDisposition.ACCEPTED, "registered through canonical fabric")

    def _receipt(self,s,d,r):
        return RegistrationReceipt(s,d,r,_digest({"service":s,"disposition":d.value,"reason":r}))

class LifecycleCoordinator:
    def __init__(self, registration: RegistrationCoordinator):
        self.registration=registration

    def transition(self, service_id: str, target: LifecycleState) -> LifecycleReceipt:
        if service_id not in self.registration.identities:
            raise ValueError("unknown service; lifecycle transition refused")
        prior=self.registration.states[service_id]
        if target not in _ALLOWED[prior]:
            return self._receipt(service_id,prior,target,False,"invalid lifecycle transition")
        if target in {LifecycleState.INITIALIZING, LifecycleState.STARTING, LifecycleState.RUNNING}:
            unresolved=[d for d in self.registration.mesh.dependencies_of(service_id)
                        if self.registration.states.get(d) not in {LifecycleState.READY,LifecycleState.RUNNING}]
            if unresolved:
                return self._receipt(service_id,prior,target,False,"dependency not ready: "+",".join(unresolved))
        self.registration.states[service_id]=target
        return self._receipt(service_id,prior,target,True,"transition accepted")

    def _receipt(self,s,p,n,a,r):
        return LifecycleReceipt(s,p,n,a,r,_digest({"service":s,"prior":p.value,"new":n.value,"accepted":a,"reason":r}))
