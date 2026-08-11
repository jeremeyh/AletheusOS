from __future__ import annotations
import asyncio, shutil
from pathlib import Path
from uuid import uuid4

class _AsyncLocalDiskAdapter:
    def __init__(self, provider, provider_id:str): self._p=provider; self.provider_id=provider_id
    async def put(self,request): return self._p.put(request)
    async def get(self,request):
        from aletheus.mammoth.contracts.providers import MammothGetRequest
        oid=request['object_id'] if isinstance(request,dict) else request.object_id
        r=self._p.get(MammothGetRequest(oid,None)); return None if r is None else {'data':r.data}
    async def health(self):
        h=self._p.health(); total=shutil.disk_usage(self._p.root).total
        return {'healthy':h.healthy,'free_bytes':h.free_bytes,'total_bytes':total,'detail':h.detail}
class _BoundaryService:
    async def persist_object(self,**kwargs): return kwargs
    async def retrieve_object(self,object_id): return {'object_id':object_id}

def _new_probe_root(project: Path) -> Path:
    run_id = uuid4().hex
    return project/'.aletheusos/mammoth/closure-probes'/run_id

def commission(project_root:str|Path):
    project=Path(project_root).expanduser().resolve()
    out=project/'reports/mammoth/genesis-113.9-closure'
    roots=_new_probe_root(project)
    from aletheus.mammoth import LocalDiskPersistenceProvider, MammothIdentityStrategy, MammothRetentionClass
    from aletheus.mammoth.identity.object_ids import MammothObjectIdFactory
    from aletheus.mammoth.contracts.providers import MammothPutRequest
    from aletheus.mammoth.closure import MammothMasterClosureGate
    data=b'ALETHEUSOS-MAMMOTH-GENESIS-113.9.2-CLOSURE-PROBE'
    m=MammothObjectIdFactory.create(namespace='system.closure',object_type='commissioning-probe',content_type='application/octet-stream',data=data,strategy=MammothIdentityStrategy.CONTENT_ADDRESSED,owner_capability='Mammoth',producer_capability='Genesis113.9.2',retention_class=MammothRetentionClass.TRANSIENT)
    req=MammothPutRequest(m,data)
    p1=_AsyncLocalDiskAdapter(LocalDiskPersistenceProvider(roots/'replica-a'),'mammoth.closure.replica-a')
    p2=_AsyncLocalDiskAdapter(LocalDiskPersistenceProvider(roots/'replica-b'),'mammoth.closure.replica-b')
    result=asyncio.run(MammothMasterClosureGate.execute(out,(p1,p2),req,_BoundaryService()))
    ep=Path(result.evidence_path)
    if not ep.is_file():raise RuntimeError('closure gate returned without durable evidence artifact')
    return ep,result.evidence_digest
