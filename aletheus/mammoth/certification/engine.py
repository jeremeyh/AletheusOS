from __future__ import annotations
import ast, hashlib, json, re
from dataclasses import asdict, dataclass
from pathlib import Path

CERT_STANDARD = "ALETHEUSOS-RAF-RSF-MAMMOTH-PROJECT-CERTIFICATION"
CLOSURE_STANDARD = "ALETHEUSOS-MAMMOTH-MASTER-CLOSURE-EVIDENCE"
CLOSURE_STATUS = "MAMMOTH_COMMISSIONING_EVIDENCE_COMPLETE"

class MammothCertificationError(RuntimeError): pass
@dataclass(frozen=True)
class CertificationCheck:
    check_id:str; passed:bool; evidence:tuple[str,...]; violations:tuple[str,...]=()
@dataclass(frozen=True)
class MammothCertificationResult:
    status:str; project_root:str; checks:tuple[CertificationCheck,...]; certified_substrate_target:str|None; refusal_reasons:tuple[str,...]; certification_digest:str

def canonical_bytes(v)->bytes:return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def sha256_bytes(b:bytes)->str:return "sha256:"+hashlib.sha256(b).hexdigest()
def sha256_file(p:Path)->str:return sha256_bytes(p.read_bytes())
def read_json(p:Path)->dict:
    try:v=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:raise MammothCertificationError(f"invalid JSON at {p}: {e}") from e
    if not isinstance(v,dict):raise MammothCertificationError(f"JSON root is not an object: {p}")
    return v

class ProjectEvidenceLocator:
    CANONICAL=Path('reports/mammoth/genesis-113.9-closure/mammoth-113.9-master-closure-evidence.json')
    @classmethod
    def locate(cls,project:Path,explicit:Path|None=None)->Path:
        p=(explicit.expanduser().resolve() if explicit else (project/cls.CANONICAL).resolve())
        if p.is_file():return p
        raise MammothCertificationError(f"mandatory Genesis 113.9 closure evidence not found: {p}")

class ClosureEvidenceVerifier:
    @staticmethod
    def verify(path:Path)->CertificationCheck:
        violations=[]; evidence=[f"path={path}",f"fileDigest={sha256_file(path)}"]
        try:doc=read_json(path)
        except MammothCertificationError as e:return CertificationCheck('CLOSURE_EVIDENCE',False,tuple(evidence),(str(e),))
        if doc.get('schemaVersion')!='1.0.0':violations.append('unexpected closure schemaVersion')
        if doc.get('standard')!=CLOSURE_STANDARD:violations.append('unexpected closure standard')
        if doc.get('status')!=CLOSURE_STATUS:violations.append('unexpected closure status')
        b=doc.get('authorityBoundary') or {}
        if b.get('mammothMayIssueRAFCertificate') is not False:violations.append('Mammoth self-certification is not explicitly prohibited')
        if b.get('rafRemainsFinalCertificationAuthority') is not True:violations.append('RAF final authority not preserved')
        body=dict(doc); declared=body.pop('evidenceDigest',None); computed=sha256_bytes(canonical_bytes(body)); evidence.append(f"computedEvidenceDigest={computed}")
        if declared!=computed:violations.append('closure evidence digest mismatch')
        d=doc.get('durability') or {}; required=int(d.get('quorum_required') or 1); verified=d.get('verified_replicas') or []
        if d.get('quorum_achieved') is not True:violations.append('closure durability quorum not achieved')
        if len(verified)<required:violations.append('verified replica count below required quorum')
        if (doc.get('telemetry') or {}).get('storage_degraded') is not False:violations.append('closure telemetry reports degraded storage')
        return CertificationCheck('CLOSURE_EVIDENCE',not violations,tuple(evidence),tuple(violations))

class PredecessorContinuityVerifier:
    REQUIRED={'113.1':('aletheus/mammoth',),'113.2':('aletheus/mammoth/providers',),'113.3':('aletheus/mammoth/lifecycle',),'113.4':('aletheus/mammoth/integrity',),'113.5':('aletheus/mammoth/indexing',),'113.6':('aletheus/mammoth/durability',),'113.7':('aletheus/mammoth/gateway',),'113.8':('aletheus/mammoth/telemetry',),'113.9':('aletheus/mammoth/closure',)}
    @classmethod
    def verify(cls,project:Path)->CertificationCheck:
        violations=[]; evidence=[]
        for version,rels in cls.REQUIRED.items():
            ok=any((project/r).exists() for r in rels); evidence.append(f"{version}:{'FOUND' if ok else 'MISSING'}")
            if not ok:violations.append(f"required installed surface missing for Genesis {version}")
        return CertificationCheck('PREDECESSOR_CONTINUITY',not violations,tuple(evidence),tuple(violations))

class ConstitutionalBoundaryVerifier:
    """AST-based boundary audit.

    The 113.9.2 scanner searched raw source lines and therefore matched its own
    regex policy declaration as though it were an executable forbidden
    capability. This verifier examines Python syntax nodes instead of string
    literals/comments, so policy text cannot self-trigger the audit.
    """
    FORBIDDEN_NAME = re.compile(r"(reason|reasoning|predict|prediction|render)", re.I)
    FORBIDDEN_CALLS = {"sign_release", "issue_certificate"}

    @classmethod
    def verify(cls, project: Path) -> CertificationCheck:
        root = project/'aletheus/mammoth'
        if not root.exists():
            return CertificationCheck('CONSTITUTIONAL_BOUNDARY', False, (), ('installed Mammoth missing',))
        violations=[]; evidence=[]; scanned=0; parsed=0
        for p in root.rglob('*.py'):
            scanned += 1
            rel = str(p.relative_to(project))
            try:
                text = p.read_text(encoding='utf-8')
                tree = ast.parse(text, filename=rel)
                parsed += 1
            except UnicodeDecodeError:
                evidence.append(f'unicodeSkipped={rel}')
                continue
            except SyntaxError as exc:
                violations.append(f'{rel}:{exc.lineno or 0}:SYNTAX_ERROR:{exc.msg}')
                continue

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if cls.FORBIDDEN_NAME.search(node.name):
                        violations.append(f'{rel}:{getattr(node, "lineno", 0)}:forbidden declaration:{node.name}')
                elif isinstance(node, ast.Call):
                    name = None
                    if isinstance(node.func, ast.Name):
                        name = node.func.id
                    elif isinstance(node.func, ast.Attribute):
                        name = node.func.attr
                    if name in cls.FORBIDDEN_CALLS:
                        violations.append(f'{rel}:{getattr(node, "lineno", 0)}:forbidden authority call:{name}')

        evidence.extend((f'pythonFilesScanned={scanned}', f'pythonFilesParsed={parsed}', 'scanner=AST_EXECUTABLE_SEMANTICS_V2'))
        return CertificationCheck('CONSTITUTIONAL_BOUNDARY', not violations, tuple(evidence), tuple(violations))

class PersistenceDomainClassifier(ast.NodeVisitor):
    """Classifies direct writes by bounded semantic destination. Unknown writes fail closed."""
    def __init__(self,rel:str):self.rel=rel; self.assignments={}; self.function=''; self.findings=[]
    def visit_FunctionDef(self,node):
        old=self.function; self.function=node.name; self.generic_visit(node); self.function=old
    visit_AsyncFunctionDef=visit_FunctionDef
    def visit_Assign(self,node):
        if len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            lit=self._path_literal(node.value)
            if lit:self.assignments[node.targets[0].id]=lit
        self.generic_visit(node)
    def _path_literal(self,node):
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='Path' and node.args and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str):return node.args[0].value
        return None
    def _receiver(self,node):
        v=node.func.value
        if isinstance(v,ast.Name):return self.assignments.get(v.id)
        if isinstance(v,ast.Call):return self._path_literal(v)
        return None
    def visit_Call(self,node):
        attr=node.func.attr if isinstance(node.func,ast.Attribute) else ''
        if attr in {'write_text','write_bytes'}:
            dest=self._receiver(node); domain='UNCLASSIFIED'
            if self.rel=='aletheus/runtime/hardening.py' and self.function=='write_documentation':domain='GENERATED_DOCUMENTATION'
            elif dest and (dest.startswith('reports/') or '/reports/' in dest):domain='DIAGNOSTIC_EVIDENCE'
            self.findings.append((node.lineno,attr,dest or '<dynamic>',domain))
        elif isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='sqlite3' and attr=='connect':self.findings.append((node.lineno,'sqlite3.connect','<database>','UNCLASSIFIED'))
        elif isinstance(node.func,ast.Name) and node.func.id=='open':self.findings.append((node.lineno,'open','<dynamic>','UNCLASSIFIED'))
        self.generic_visit(node)

class PersistenceBypassVerifier:
    CONSUMERS=('aletheus/memory','aletheus/knowledge','aletheus/knowledge_graph','aletheus/applications','aletheus/runtime')
    SKIP=('/tests/','/tools/','/backup/','/diagnostics/','/migrations/','/__pycache__/')
    @classmethod
    def verify(cls,project:Path)->CertificationCheck:
        violations=[]; evidence=[]; scanned=0; classified=0
        for rr in cls.CONSUMERS:
            base=project/rr
            if not base.exists():continue
            for p in base.rglob('*.py'):
                rel=str(p.relative_to(project)); norm='/'+rel+'/'
                if any(x in norm for x in cls.SKIP):continue
                scanned+=1
                try:tree=ast.parse(p.read_text(encoding='utf-8'),filename=rel)
                except (UnicodeDecodeError,SyntaxError) as e:violations.append(f'{rel}:scan-error:{e}');continue
                v=PersistenceDomainClassifier(rel);v.visit(tree)
                for line,kind,dest,domain in v.findings:
                    classified+=1; evidence.append(f'{domain}:{rel}:{line}:{kind}:{dest}')
                    if domain=='UNCLASSIFIED':violations.append(f'{rel}:{line}:{kind}:{dest}:UNCLASSIFIED_DIRECT_IO')
        evidence.insert(0,f'consumerFilesScanned={scanned}');evidence.insert(1,f'directIOFindingsClassified={classified}')
        evidence.append('policy=CANONICAL_PLATFORM_DATA requires Mammoth; bounded diagnostic/documentation output permitted; UNCLASSIFIED fails closed')
        return CertificationCheck('PERSISTENCE_DOMAIN_CLASSIFICATION',not violations,tuple(evidence),tuple(violations))

class MammothProjectLevelCertificationEngine:
    @classmethod
    def certify(cls,*,project_root,output_directory,inspected_at_iso,closure_evidence=None):
        project=Path(project_root).expanduser().resolve();out=Path(output_directory).expanduser().resolve();out.mkdir(parents=True,exist_ok=True)
        if not project.exists():raise MammothCertificationError(f'project root not found: {project}')
        try:closure_check=ClosureEvidenceVerifier.verify(ProjectEvidenceLocator.locate(project,Path(closure_evidence) if closure_evidence else None))
        except MammothCertificationError as e:closure_check=CertificationCheck('CLOSURE_EVIDENCE',False,(),(str(e),))
        checks=(ConstitutionalBoundaryVerifier.verify(project),PersistenceBypassVerifier.verify(project),PredecessorContinuityVerifier.verify(project),closure_check)
        refusals=tuple(f'{c.check_id}: {v}' for c in checks for v in c.violations);status='CERTIFIED' if all(c.passed for c in checks) else 'REFUSED'
        body={'schemaVersion':'1.0.0','standard':CERT_STANDARD,'release':'Genesis 113.9.2','status':status,'projectRoot':str(project),'inspectedAtIso':inspected_at_iso,'checks':[asdict(c) for c in checks],'certifiedSubstrateTarget':str(project/'aletheus/mammoth') if status=='CERTIFIED' else None,'refusalReasons':list(refusals),'authorityBoundary':{'certificationIssuedBy':'RAF_RSF_PROJECT_LEVEL_GATE','mammothSelfCertification':False}}
        digest=sha256_bytes(canonical_bytes(body));(out/'mammoth-project-certification.json').write_text(json.dumps({**body,'certificationDigest':digest},indent=2,sort_keys=True)+'\n',encoding='utf-8')
        return MammothCertificationResult(status,str(project),checks,body['certifiedSubstrateTarget'],refusals,digest)
