from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any
class GatewayError(RuntimeError): pass
class ConsumerIdentity(str,Enum):
    MEMORY_ENGINE='MEMORY_ENGINE'; KNOWLEDGE_ENGINE='KNOWLEDGE_ENGINE'; OPUS='OPUS'; APPLICATION_RUNTIME='APPLICATION_RUNTIME'; PLATFORM_SERVICE='PLATFORM_SERVICE'
@dataclass(frozen=True)
class ConsumerPolicy:
    consumer:ConsumerIdentity; allowed_namespace_prefixes:tuple[str,...]; may_persist:bool=True; may_retrieve:bool=True
class CanonicalConsumptionGateway:
    def __init__(self,service:Any,policies:tuple[ConsumerPolicy,...]): self.service=service; self._policies={p.consumer:p for p in policies}
    def _policy(self,c):
        if c not in self._policies: raise GatewayError(f'consumer not registered: {c}')
        return self._policies[c]
    @staticmethod
    def _allowed(ns,prefixes): return any(ns==p or ns.startswith(p+'.') for p in prefixes)
    async def persist(self,consumer:ConsumerIdentity,*,namespace:str,**kwargs):
        p=self._policy(consumer)
        if not p.may_persist: raise GatewayError('consumer persistence permission denied')
        if not self._allowed(namespace,p.allowed_namespace_prefixes): raise GatewayError('namespace denied')
        producer=kwargs.pop('producer_capability',consumer.value)
        return await self.service.persist_object(namespace=namespace,owner_capability=consumer.value,producer_capability=producer,**kwargs)
    async def retrieve(self,consumer:ConsumerIdentity,object_id:str):
        if not self._policy(consumer).may_retrieve: raise GatewayError('consumer retrieval permission denied')
        return await self.service.retrieve_object(object_id)
def default_consumer_policies():
    return (ConsumerPolicy(ConsumerIdentity.MEMORY_ENGINE,('memory','system.memory')),ConsumerPolicy(ConsumerIdentity.KNOWLEDGE_ENGINE,('knowledge','system.knowledge')),ConsumerPolicy(ConsumerIdentity.OPUS,('opus','system.opus')),ConsumerPolicy(ConsumerIdentity.APPLICATION_RUNTIME,('application','system.application')),ConsumerPolicy(ConsumerIdentity.PLATFORM_SERVICE,('platform','system')))
