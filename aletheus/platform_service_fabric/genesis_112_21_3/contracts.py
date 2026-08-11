from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Protocol, runtime_checkable, Any, Mapping, Sequence
import hashlib, json

STANDARD="ALETHEUSOS-GENESIS-112.21.3-CANONICAL-SERVICE-CONTRACT"

class ServiceAuthority(str, Enum):
    SERVICE_DISCOVERY="SERVICE_DISCOVERY"
    SERVICE_REGISTRATION="SERVICE_REGISTRATION"
    ENGINE_REGISTRATION="ENGINE_REGISTRATION"
    LIFECYCLE_COORDINATION="LIFECYCLE_COORDINATION"
    RUNTIME_INSPECTION="RUNTIME_INSPECTION"
    RELIABILITY_OBSERVATION="RELIABILITY_OBSERVATION"

class BindingDisposition(str, Enum):
    COMPOSE="COMPOSE"
    REFACTOR_BEHIND_CONTRACT="REFACTOR_BEHIND_CONTRACT"
    REUSE_BEHIND_CONTRACT="REUSE_BEHIND_CONTRACT"
    EXCLUDE_NON_CANONICAL="EXCLUDE_NON_CANONICAL"

@dataclass(frozen=True)
class ServiceIdentity:
    service_id:str
    owner_domain:str
    authority:ServiceAuthority
    source_surfaces:tuple[str,...]
    lifecycle_owner:str
    reliability_owner:str="RSF"
    persistence_owner:str="MAMMOTH"
    release_authority:str="RAF"

@dataclass(frozen=True)
class ServiceDescriptor:
    identity:ServiceIdentity
    capabilities:tuple[str,...]
    dependencies:tuple[str,...]=()
    observability_hooks:tuple[str,...]=()
    disposition:BindingDisposition=BindingDisposition.REUSE_BEHIND_CONTRACT
    notes:tuple[str,...]=()

@dataclass(frozen=True)
class BindingEvidence:
    schemaVersion:str
    standard:str
    predecessorEvidenceDigest:str
    descriptors:tuple[ServiceDescriptor,...]
    runtimeRegistryDisposition:str
    runtimeCoreMutationRequired:bool
    sourceReplacementRequired:bool

    def canonical_digest(self)->str:
        def default(o):
            if isinstance(o, Enum): return o.value
            if hasattr(o,"__dataclass_fields__"): return asdict(o)
            raise TypeError(type(o))
        raw=json.dumps(self,sort_keys=True,separators=(",",":"),default=default).encode()
        return "sha256:"+hashlib.sha256(raw).hexdigest()

@runtime_checkable
class ServiceDiscoveryContract(Protocol):
    def resolve(self, service_id:str) -> Any | None: ...
    def list_services(self) -> Sequence[str]: ...

@runtime_checkable
class ServiceRegistrationContract(Protocol):
    def register(self, service_id:str, service:Any) -> Any: ...
    def unregister(self, service_id:str) -> Any: ...

@runtime_checkable
class EngineRegistrationContract(Protocol):
    def register_engine(self, engine_id:str, engine:Any) -> Any: ...
    def get_engine(self, engine_id:str) -> Any | None: ...

@runtime_checkable
class LifecycleContract(Protocol):
    def start(self, component_id:str) -> Any: ...
    def stop(self, component_id:str) -> Any: ...
    def status(self, component_id:str) -> Any: ...

@runtime_checkable
class RuntimeInspectionContract(Protocol):
    def inspect(self, subject:Any=None) -> Any: ...

@runtime_checkable
class ReliabilityObservationPort(Protocol):
    def observe(self, component_id:str) -> Mapping[str,Any]: ...
