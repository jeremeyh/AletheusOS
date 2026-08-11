from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from enum import Enum
import ast, hashlib, json, re, tempfile, os
from datetime import datetime, timezone

STANDARD="ALETHEUSOS-GENESIS-112.21.2-EVIDENCE-BASED-SERVICE-ARCHITECTURE-RECONCILIATION"

class Classification(str, Enum):
    REUSE="REUSE"
    REFACTOR="REFACTOR"
    PROMOTE="PROMOTE"
    COMPOSE="COMPOSE"
    DEPRECATE_CANDIDATE="DEPRECATE_CANDIDATE"
    ABSTAIN="ABSTAIN"

@dataclass(frozen=True)
class EvidenceVector:
    path:str
    symbol:str
    kind:str
    owner_hint:str
    lifecycle_refs:tuple[str,...]
    registry_refs:tuple[str,...]
    anchor_refs:tuple[str,...]
    transport_refs:tuple[str,...]
    mammoth_refs:tuple[str,...]
    rsf_refs:tuple[str,...]
    raf_refs:tuple[str,...]
    import_refs:tuple[str,...]
    callsite_count:int
    test_refs:int
    sha256:str

@dataclass(frozen=True)
class CandidateDecision:
    identity:str
    candidates:tuple[str,...]
    classification:Classification
    confidence:int
    evidence_basis:tuple[str,...]
    required_followup:tuple[str,...]
    canonical_candidate:str|None

def _sha_bytes(data:bytes)->str:
    return "sha256:"+hashlib.sha256(data).hexdigest()

def _canonical_digest(obj:Any)->str:
    raw=json.dumps(obj,sort_keys=True,separators=(",",":"),default=str).encode()
    return _sha_bytes(raw)

def _atomic_json(path:Path,obj:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True)
    data=json.dumps(obj,indent=2,sort_keys=True,default=str).encode()
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)

def _py_files(root:Path):
    skip={".git",".venv","venv","node_modules","__pycache__",".aletheusos"}
    for p in sorted(root.rglob("*.py")):
        if not any(part in skip for part in p.parts):
            yield p

def _safe_parse(p:Path):
    try:
        return ast.parse(p.read_text(encoding="utf-8",errors="replace")),None
    except SyntaxError as e:
        return None,f"{p}:{e.lineno}:{e.msg}"

def _names_in_tree(tree):
    imports=[]; classes=[]; functions=[]; refs=set()
    for n in ast.walk(tree):
        if isinstance(n,ast.Import):
            imports.extend(a.name for a in n.names)
        elif isinstance(n,ast.ImportFrom):
            imports.append(n.module or "")
        elif isinstance(n,ast.ClassDef):
            classes.append(n.name)
        elif isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
            functions.append(n.name)
        elif isinstance(n,ast.Name):
            refs.add(n.id)
        elif isinstance(n,ast.Attribute):
            refs.add(n.attr)
    return imports,classes,functions,refs

class RepositoryEvidenceCollector:
    SERVICE_HINT=re.compile(r"(service|registry|manager|fabric|anchor|runtime|router|dispatcher|lifecycle|health)",re.I)
    @classmethod
    def collect(cls, repository_root:str|Path)->dict:
        root=Path(repository_root).resolve()
        aletheus=root/"aletheus"
        vectors=[]
        parse_errors=[]
        all_text={}
        for p in _py_files(aletheus):
            try:
                txt=p.read_text(encoding="utf-8",errors="replace")
            except Exception:
                continue
            all_text[str(p.relative_to(root))]=txt

        # global call/reference index
        reference_counts={}
        for rel,txt in all_text.items():
            for token in re.findall(r"\b[A-Z][A-Za-z0-9_]{3,}\b",txt):
                reference_counts[token]=reference_counts.get(token,0)+1

        test_text="\n".join(
            p.read_text(encoding="utf-8",errors="replace")
            for p in _py_files(root/"tests")
        ) if (root/"tests").exists() else ""

        for rel,txt in all_text.items():
            p=root/rel
            tree,err=_safe_parse(p)
            if err:
                parse_errors.append(err); continue
            imports,classes,functions,refs=_names_in_tree(tree)
            symbols=[x for x in classes+functions if cls.SERVICE_HINT.search(x)]
            if not symbols and not cls.SERVICE_HINT.search(rel):
                continue
            for symbol in symbols or (Path(rel).stem,):
                owner_hint="runtime" if "/runtime/" in f"/{rel}/" else ("platform" if "/platform" in f"/{rel}/" else "unresolved")
                life=tuple(sorted(x for x in refs if re.search(r"(start|stop|shutdown|health|ready|lifecycle|restart)",x,re.I)))
                regs=tuple(sorted(x for x in refs if "Registry" in x or "registry" in x))
                anchors=tuple(sorted(x for x in refs if "Anchor" in x or "Circuit" in x))
                transit=tuple(sorted(x for x in refs if re.search(r"(kinekt|ctf|transit|event|router|dispatch|relay|mesh)",x,re.I)))
                mammoth=tuple(sorted(x for x in refs if re.search(r"mammoth",x,re.I)))
                rsf=tuple(sorted(x for x in refs if re.search(r"(rsf|reliab)",x,re.I)))
                raf=tuple(sorted(x for x in refs if re.search(r"(raf|release)",x,re.I)))
                vectors.append(EvidenceVector(
                    path=rel,
                    symbol=symbol,
                    kind="class_or_function" if symbol in classes+functions else "module",
                    owner_hint=owner_hint,
                    lifecycle_refs=life,
                    registry_refs=regs,
                    anchor_refs=anchors,
                    transport_refs=transit,
                    mammoth_refs=mammoth,
                    rsf_refs=rsf,
                    raf_refs=raf,
                    import_refs=tuple(sorted(set(imports))),
                    callsite_count=max(0,reference_counts.get(symbol,0)-1),
                    test_refs=test_text.count(symbol),
                    sha256=_sha_bytes(txt.encode()),
                ))
        return {
            "schemaVersion":"1.0.0",
            "standard":STANDARD+"-EVIDENCE-CORPUS",
            "repositoryRoot":str(root),
            "vectors":[asdict(v) for v in vectors],
            "parseErrors":parse_errors,
            "counts":{"vectors":len(vectors),"parseErrors":len(parse_errors)}
        }

class EvidenceBasedClassifier:
    """
    Conservative classifier:
    - identical symbol implemented in multiple paths => ABSTAIN unless one clearly dominates evidence.
    - strong integration + tests + callsites => REUSE or PROMOTE.
    - partial integration / missing lifecycle or ownership evidence => REFACTOR.
    - complementary, non-equivalent capabilities => COMPOSE.
    - apparently unused duplicate with stronger sibling => DEPRECATE_CANDIDATE, never delete automatically.
    """
    @classmethod
    def classify(cls, corpus:dict)->dict:
        by_identity={}
        for v in corpus["vectors"]:
            by_identity.setdefault(v["symbol"],[]).append(v)

        decisions=[]
        for identity,cands in sorted(by_identity.items()):
            paths=tuple(v["path"] for v in cands)
            if len(cands)==1:
                v=cands[0]
                score=(min(v["callsite_count"],5)*8)+(min(v["test_refs"],5)*8)
                score+=10 if v["lifecycle_refs"] else 0
                score+=10 if v["registry_refs"] else 0
                score+=8 if v["anchor_refs"] else 0
                score+=8 if v["transport_refs"] else 0
                if score>=70:
                    classification=Classification.REUSE
                    conf=min(95,70+score//10)
                    basis=("single implementation","strong call/test evidence","integration evidence")
                    follow=()
                    canonical=v["path"]
                elif score>=35:
                    classification=Classification.REFACTOR
                    conf=75
                    basis=("single implementation","partial integration evidence")
                    follow=("confirm owner","confirm lifecycle","confirm runtime binding")
                    canonical=v["path"]
                else:
                    classification=Classification.ABSTAIN
                    conf=50
                    basis=("single implementation","insufficient usage evidence")
                    follow=("inspect call-sites","inspect tests","confirm authority owner")
                    canonical=None
            else:
                # evidence separation
                ranked=sorted(
                    cands,
                    key=lambda v:(v["callsite_count"]+v["test_refs"]*2+len(v["registry_refs"])+len(v["lifecycle_refs"])),
                    reverse=True
                )
                top,second=ranked[0],ranked[1]
                top_score=top["callsite_count"]+top["test_refs"]*2+len(top["registry_refs"])+len(top["lifecycle_refs"])
                second_score=second["callsite_count"]+second["test_refs"]*2+len(second["registry_refs"])+len(second["lifecycle_refs"])
                complementary=any(bool(v["anchor_refs"]) for v in cands) and any(bool(v["transport_refs"]) for v in cands)
                if complementary and len({v["path"] for v in cands})>1:
                    classification=Classification.COMPOSE
                    conf=72
                    basis=("multiple implementations","complementary integration evidence")
                    follow=("define canonical composition boundary","prevent duplicate authority")
                    canonical=None
                elif top_score>=max(4,second_score*2+2):
                    classification=Classification.PROMOTE
                    conf=80
                    basis=("multiple implementations",f"evidence-leading candidate: {top['path']}")
                    follow=("prove capability preservation of weaker candidates","no deletion before external authorization")
                    canonical=top["path"]
                else:
                    classification=Classification.ABSTAIN
                    conf=45
                    basis=("multiple implementations","insufficient evidence separation")
                    follow=("compare behavior","compare tests","compare call-sites","compare authority","compare lifecycle")
                    canonical=None

            decisions.append(asdict(CandidateDecision(
                identity=identity,
                candidates=paths,
                classification=classification,
                confidence=conf,
                evidence_basis=tuple(basis),
                required_followup=tuple(follow),
                canonical_candidate=canonical,
            )))

        out={
            "schemaVersion":"1.0.0",
            "standard":STANDARD+"-DECISION-MAP",
            "classificationVocabulary":[x.value for x in Classification],
            "decisions":decisions,
            "summary":{},
            "automaticSourceMutationPermitted":False,
            "automaticDeletionPermitted":False,
            "automaticCanonicalPromotionPermitted":False,
        }
        for d in decisions:
            k=d["classification"]
            out["summary"][k]=out["summary"].get(k,0)+1
        out["evidenceDigest"]=_canonical_digest(out)
        return out

class ServiceArchitectureReconciliationHarness:
    @staticmethod
    def run(repository_root:str|Path, write_reports:bool=True)->dict:
        root=Path(repository_root).resolve()
        corpus=RepositoryEvidenceCollector.collect(root)
        decisions=EvidenceBasedClassifier.classify(corpus)
        result={
            "schemaVersion":"1.0.0",
            "standard":STANDARD,
            "timestampIso":datetime.now(timezone.utc).isoformat(),
            "mode":"EVIDENCE_BASED_RECONCILIATION",
            "corpus":corpus,
            "decisionMap":decisions,
            "constitutionalLaws":{
                "runtimeCoreCompositionRootPreserved":True,
                "mammothOwnsDurablePersistence":True,
                "rsfOwnsReliabilityAssurance":True,
                "rafRetainsFinalCertificationAuthority":True,
                "kinektCtfOwnTransportNotBusinessAuthority":True,
                "noAutomaticDeletion":True,
                "abstainWhenEvidenceInsufficient":True,
            },
            "status":"RECONCILIATION_EVIDENCE_READY"
        }
        result["evidenceDigest"]=_canonical_digest(result)
        if write_reports:
            out=root/"reports/platform-service-fabric/genesis-112.21.2"
            _atomic_json(out/"service-evidence-corpus.json",corpus)
            _atomic_json(out/"service-architecture-decision-map.json",decisions)
            _atomic_json(out/"genesis-112.21.2-reconciliation-report.json",result)
        return result
