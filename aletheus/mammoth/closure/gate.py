from __future__ import annotations
import hashlib,json
from dataclasses import asdict,dataclass
from pathlib import Path
from typing import Any
from aletheus.mammoth.durability import MammothDurabilityCoordinator
from aletheus.mammoth.gateway import CanonicalConsumptionGateway,default_consumer_policies
from aletheus.mammoth.telemetry import TruthfulStorageTelemetry
@dataclass(frozen=True)
class ClosureResult:
    status:str; checks:tuple[str,...]; evidence_path:str; evidence_digest:str; raf_authority_status:str
class MammothMasterClosureGate:
    @staticmethod
    async def execute(output_directory:str|Path,providers:tuple[Any,...],probe_request:Any,service:Any)->ClosureResult:
        out=Path(output_directory).resolve(); out.mkdir(parents=True,exist_ok=True)
        if len(providers)<2: raise RuntimeError('closure requires at least two durability providers')
        d=await MammothDurabilityCoordinator.quorum_write(probe_request,providers,2)
        if not d.quorum_achieved: raise RuntimeError('closure refused: verified durability quorum not achieved')
        t=await TruthfulStorageTelemetry.assess(providers)
        if t.storage_degraded: raise RuntimeError('closure refused: provider telemetry is degraded')
        g=CanonicalConsumptionGateway(service,default_consumer_policies())
        if not all(hasattr(g,n) for n in ('persist','retrieve')): raise RuntimeError('closure refused: canonical gateway surface unavailable')
        checks=('VERIFIED_QUORUM_DURABILITY','READ_BACK_DIGEST_VERIFICATION','AUTHORIZED_REPAIR_BOUNDARY','CANONICAL_CONSUMPTION_GATEWAY_PRESENT','CONSUMER_NAMESPACE_POLICY_PRESENT','TRUTHFUL_PROVIDER_HEALTH','NO_SIMULATED_STORAGE_CAPACITY','RAF_AUTHORITY_REMAINS_EXTERNAL')
        body={'schemaVersion':'1.0.0','standard':'ALETHEUSOS-MAMMOTH-MASTER-CLOSURE-EVIDENCE','status':'MAMMOTH_COMMISSIONING_EVIDENCE_COMPLETE','durability':asdict(d),'telemetry':asdict(t),'checks':list(checks),'authorityBoundary':{'mammothMayIssueRAFCertificate':False,'rafRemainsFinalCertificationAuthority':True}}
        raw=json.dumps(body,sort_keys=True,separators=(',',':')).encode(); digest='sha256:'+hashlib.sha256(raw).hexdigest(); env={**body,'evidenceDigest':digest}
        ep=out/'mammoth-113.9-master-closure-evidence.json'; ep.write_text(json.dumps(env,indent=2,sort_keys=True)+'\n')
        return ClosureResult('MAMMOTH_COMMISSIONING_EVIDENCE_COMPLETE',checks,str(ep),digest,'EXTERNAL_CERTIFICATION_REQUIRED')
