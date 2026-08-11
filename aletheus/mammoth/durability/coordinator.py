from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Any
class DurabilityError(RuntimeError): pass
@dataclass(frozen=True)
class ReplicaObservation:
    provider_id:str; write_ok:bool; readable:bool; digest_matches:bool; error:str=''
@dataclass(frozen=True)
class RepairPlan:
    object_id:str; authoritative_digest:str; source_provider_id:str; target_provider_ids:tuple[str,...]; executable:bool=False; authority_ref:str|None=None
@dataclass(frozen=True)
class DurabilityResult:
    quorum_required:int; quorum_achieved:bool; successful_writes:tuple[str,...]; degraded_providers:tuple[str,...]; verified_replicas:tuple[str,...]; observations:tuple[ReplicaObservation,...]; repair_plan:RepairPlan|None

def _sha(data:bytes)->str: return 'sha256:'+hashlib.sha256(data).hexdigest()
def _data(x):
    if x is None:return None
    if isinstance(x,(bytes,bytearray)):return bytes(x)
    if isinstance(x,dict): return bytes(x['data']) if 'data' in x else None
    return bytes(x.data) if hasattr(x,'data') else None
def _put_ok(x):
    if isinstance(x,bool):return x
    if isinstance(x,dict):return bool(x.get('success'))
    if hasattr(x,'success'):return bool(x.success)
    return x is not None
class MammothDurabilityCoordinator:
    @staticmethod
    async def quorum_write(request:Any,providers:tuple[Any,...],quorum_count:int)->DurabilityResult:
        if quorum_count<1: raise DurabilityError('quorum_count must be >= 1')
        if len(providers)<quorum_count: raise DurabilityError('available provider count is less than required quorum')
        meta=request['metadata'] if isinstance(request,dict) else request.metadata
        oid=meta.get('object_id') if isinstance(meta,dict) else getattr(meta,'object_id',None)
        data=bytes(request['data'] if isinstance(request,dict) else request.data)
        digest=_sha(data); successful=[]; degraded=[]; errors={}
        for p in providers:
            try:
                r=await p.put(request)
                if _put_ok(r): successful.append(p.provider_id)
                else: degraded.append(p.provider_id); errors[p.provider_id]='provider reported unsuccessful write'
            except Exception as e: degraded.append(p.provider_id); errors[p.provider_id]=str(e)
        obs=[]; verified=[]
        for p in providers:
            if p.provider_id not in successful:
                obs.append(ReplicaObservation(p.provider_id,False,False,False,errors.get(p.provider_id,'write failed'))); continue
            try:
                payload=_data(await p.get({'object_id':oid})); readable=payload is not None; matches=readable and _sha(payload)==digest
                if matches: verified.append(p.provider_id)
                else: degraded.append(p.provider_id)
                obs.append(ReplicaObservation(p.provider_id,True,readable,bool(matches),'' if matches else 'read-back digest verification failed'))
            except Exception as e: degraded.append(p.provider_id); obs.append(ReplicaObservation(p.provider_id,True,False,False,str(e)))
        degraded=list(dict.fromkeys(degraded)); quorum=len(verified)>=quorum_count; plan=None
        if quorum and degraded: plan=RepairPlan(oid,digest,verified[0],tuple(degraded),False,None)
        return DurabilityResult(quorum_count,quorum,tuple(successful),tuple(degraded),tuple(verified),tuple(obs),plan)
    @staticmethod
    def authorize_repair(plan:RepairPlan,authority_ref:str)->RepairPlan:
        if not authority_ref.strip(): raise DurabilityError('repair authorization reference is required')
        return RepairPlan(plan.object_id,plan.authoritative_digest,plan.source_provider_id,plan.target_provider_ids,True,authority_ref)
    @staticmethod
    async def execute_repair(plan:RepairPlan,request:Any,providers:tuple[Any,...])->tuple[str,...]:
        if not plan.executable or not plan.authority_ref: raise DurabilityError('repair plan is not authorized')
        pmap={p.provider_id:p for p in providers}; src=pmap.get(plan.source_provider_id)
        if src is None: raise DurabilityError('repair source provider unavailable')
        payload=_data(await src.get({'object_id':plan.object_id}))
        if payload is None or _sha(payload)!=plan.authoritative_digest: raise DurabilityError('repair source failed authoritative digest verification')
        repaired=[]
        for pid in plan.target_provider_ids:
            p=pmap.get(pid)
            if p is None: continue
            await p.put(request); verify=_data(await p.get({'object_id':plan.object_id}))
            if verify is not None and _sha(verify)==plan.authoritative_digest: repaired.append(pid)
        return tuple(repaired)
