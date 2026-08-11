from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
from .contracts import *

PREDECESSOR_EXPECTED_DIGEST="sha256:3045f58c72e87e58d525f10a3d1f971bb2dbb7d4553d6f216908b449fcf734b2"

CANONICAL_BINDING_DESCRIPTORS=(
    ServiceDescriptor(
        identity=ServiceIdentity(
            service_id="platform.service.discovery",
            owner_domain="AletheusOS Runtime",
            authority=ServiceAuthority.SERVICE_DISCOVERY,
            source_surfaces=(
                "aletheus/runtime/registries.py",
                "aletheus/runtime/services/service_registry.py",
            ),
            lifecycle_owner="LifecycleManager",
        ),
        capabilities=("resolve","list_services","service metadata lookup"),
        disposition=BindingDisposition.COMPOSE,
        notes=(
            "ServiceRegistry surfaces are complementary and must be composed.",
            "Neither implementation is deleted, overwritten, or silently promoted.",
        ),
    ),
    ServiceDescriptor(
        identity=ServiceIdentity(
            service_id="platform.service.registration",
            owner_domain="AletheusOS Runtime",
            authority=ServiceAuthority.SERVICE_REGISTRATION,
            source_surfaces=("aletheus/runtime/managers/registration_manager.py",),
            lifecycle_owner="LifecycleManager",
        ),
        capabilities=("register","unregister","bounded registration orchestration"),
        disposition=BindingDisposition.REFACTOR_BEHIND_CONTRACT,
    ),
    ServiceDescriptor(
        identity=ServiceIdentity(
            service_id="platform.engine.registration",
            owner_domain="AletheusOS Runtime",
            authority=ServiceAuthority.ENGINE_REGISTRATION,
            source_surfaces=("aletheus/runtime/registries.py",),
            lifecycle_owner="LifecycleManager",
        ),
        capabilities=("register_engine","get_engine","engine inventory"),
        disposition=BindingDisposition.REFACTOR_BEHIND_CONTRACT,
        notes=("EngineRegistry remains distinct from ServiceRegistry authority.",),
    ),
    ServiceDescriptor(
        identity=ServiceIdentity(
            service_id="platform.lifecycle.coordination",
            owner_domain="AletheusOS Runtime",
            authority=ServiceAuthority.LIFECYCLE_COORDINATION,
            source_surfaces=("aletheus/runtime/managers/lifecycle_manager.py",),
            lifecycle_owner="LifecycleManager",
        ),
        capabilities=("start","stop","status","lifecycle transition coordination"),
        disposition=BindingDisposition.REFACTOR_BEHIND_CONTRACT,
        notes=("LifecycleManager authority is formalized without forcing runtime/core.py mutation.",),
    ),
    ServiceDescriptor(
        identity=ServiceIdentity(
            service_id="platform.runtime.inspection",
            owner_domain="AletheusOS Runtime",
            authority=ServiceAuthority.RUNTIME_INSPECTION,
            source_surfaces=(
                "aletheus/runtime/inspector/runtime_inspector.py",
                "aletheus/runtime/managers/runtime_inspector.py",
            ),
            lifecycle_owner="LifecycleManager",
        ),
        capabilities=("inspect","diagnostic view","manager-level runtime view"),
        disposition=BindingDisposition.COMPOSE,
        notes=("Distinct RuntimeInspector capabilities are composed by capability.",),
    ),
    ServiceDescriptor(
        identity=ServiceIdentity(
            service_id="platform.reliability.observation",
            owner_domain="RSF",
            authority=ServiceAuthority.RELIABILITY_OBSERVATION,
            source_surfaces=("aletheus/rsf/genesis_112_20/observation.py",),
            lifecycle_owner="RSF",
            reliability_owner="RSF",
        ),
        capabilities=("observe","reliability evidence only"),
        disposition=BindingDisposition.REFACTOR_BEHIND_CONTRACT,
        notes=(
            "Service Fabric consumes reliability evidence; it does not absorb RSF authority.",
            "RAF remains external final certification authority.",
        ),
    ),
)

RUNTIME_REGISTRY_DESCRIPTOR=ServiceDescriptor(
    identity=ServiceIdentity(
        service_id="legacy.mesh.runtime_registry",
        owner_domain="Legacy/Dormant Mesh",
        authority=ServiceAuthority.SERVICE_DISCOVERY,
        source_surfaces=("aletheus/mesh/runtime_registry.py",),
        lifecycle_owner="none",
    ),
    capabilities=(),
    disposition=BindingDisposition.EXCLUDE_NON_CANONICAL,
    notes=(
        "Genesis 112.21.2.3 classified RuntimeRegistry as LEGACY_INACTIVE.",
        "Preserved non-destructively; excluded from canonical platform service authority.",
    ),
)

@dataclass(frozen=True)
class CompositeBinding:
    binding_id:str
    primary:Any
    secondary:Any
    resolver:Callable[[Any,Any,str],Any] | None = None

    def invoke(self, method:str, *args, **kwargs):
        p=getattr(self.primary,method,None)
        s=getattr(self.secondary,method,None)
        if p and s and self.resolver:
            return self.resolver(p,s,method)(*args,**kwargs)
        if p: return p(*args,**kwargs)
        if s: return s(*args,**kwargs)
        raise AttributeError(f"{self.binding_id}: method '{method}' unavailable on composed surfaces")

class CanonicalBindingRegistry:
    def __init__(self):
        self._bindings={}
        self._descriptors={d.identity.service_id:d for d in CANONICAL_BINDING_DESCRIPTORS}

    def descriptors(self):
        return tuple(self._descriptors.values())

    def descriptor(self, service_id:str):
        return self._descriptors.get(service_id)

    def bind(self, service_id:str, implementation:Any):
        if service_id not in self._descriptors:
            raise KeyError(f"Unknown canonical service id: {service_id}")
        self._bindings[service_id]=implementation

    def bind_composite(self, service_id:str, primary:Any, secondary:Any, resolver=None):
        d=self.descriptor(service_id)
        if d is None or d.disposition != BindingDisposition.COMPOSE:
            raise ValueError(f"{service_id} is not declared as a composed binding")
        self._bindings[service_id]=CompositeBinding(service_id,primary,secondary,resolver)

    def resolve(self, service_id:str):
        return self._bindings.get(service_id)

    def evidence(self)->BindingEvidence:
        return BindingEvidence(
            schemaVersion="1.0.0",
            standard=STANDARD,
            predecessorEvidenceDigest=PREDECESSOR_EXPECTED_DIGEST,
            descriptors=CANONICAL_BINDING_DESCRIPTORS,
            runtimeRegistryDisposition=RUNTIME_REGISTRY_DESCRIPTOR.disposition.value,
            runtimeCoreMutationRequired=False,
            sourceReplacementRequired=False,
        )
