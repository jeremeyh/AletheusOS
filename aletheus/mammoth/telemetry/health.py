from __future__ import annotations
import os,time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
@dataclass(frozen=True)
class ProviderHealthObservation:
    provider_id:str; healthy:bool; free_bytes:int|None; total_bytes:int|None; latency_ms:float; error:str=''
@dataclass(frozen=True)
class StorageHealthReport:
    observed_at_epoch_ms:int; total_providers:int; healthy_providers:int; degraded_providers:int; storage_degraded:bool; observations:tuple[ProviderHealthObservation,...]; free_bytes_known:int; total_bytes_known:int
class TruthfulStorageTelemetry:
    @staticmethod
    async def assess(providers:tuple[Any,...])->StorageHealthReport:
        obs=[]
        for p in providers:
            t=time.perf_counter()
            try:
                h=await p.health(); ms=(time.perf_counter()-t)*1000
                if isinstance(h,dict): healthy=bool(h.get('healthy')); free=h.get('free_bytes',h.get('freeBytes')); total=h.get('total_bytes',h.get('totalBytes'))
                else: healthy=bool(getattr(h,'healthy',False)); free=getattr(h,'free_bytes',getattr(h,'freeBytes',None)); total=getattr(h,'total_bytes',getattr(h,'totalBytes',None))
                obs.append(ProviderHealthObservation(p.provider_id,healthy,free,total,ms))
            except Exception as e: obs.append(ProviderHealthObservation(p.provider_id,False,None,None,(time.perf_counter()-t)*1000,str(e)))
        hc=sum(x.healthy for x in obs)
        return StorageHealthReport(int(time.time()*1000),len(obs),hc,len(obs)-hc,hc!=len(obs),tuple(obs),sum(x.free_bytes for x in obs if isinstance(x.free_bytes,int)),sum(x.total_bytes for x in obs if isinstance(x.total_bytes,int)))
    @staticmethod
    def filesystem_capacity(path:str|Path):
        p=Path(path).resolve(); p.mkdir(parents=True,exist_ok=True); st=os.statvfs(p); return st.f_bavail*st.f_frsize,st.f_blocks*st.f_frsize
