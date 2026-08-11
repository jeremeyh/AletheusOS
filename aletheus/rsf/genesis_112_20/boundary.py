from __future__ import annotations
import ast
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class BoundaryFinding:
    path: str
    line: int
    rule_id: str
    detail: str

@dataclass(frozen=True)
class BoundaryCertificationResult:
    passed: bool
    files_scanned: int
    findings: tuple[BoundaryFinding, ...]

class RAFRSFConstitutionalBoundaryCertification:
    """
    AST-based structural audit. It avoids matching comments, policy strings, or
    the scanner's own regex/source text.

    RSF may assess reliability and emit evidence.
    RSF may not sign/issue release certificates.
    RAF may consume RSF evidence.
    RAF may not implement RSF reliability state machines.
    """
    RSF_FORBIDDEN_CALLS = {"sign_release", "issue_release_certificate", "publish_release_certificate"}
    RAF_FORBIDDEN_NAMES = {"ReliabilityFailureDomainEngine", "RSFRecoveryContinuityEngine"}

    @classmethod
    def scan(cls, project_root: str | Path) -> BoundaryCertificationResult:
        project = Path(project_root).resolve()
        roots = []
        for rel in ("aletheus/rsf", "aletheus/reliability", "aletheus/release", "aletheus/raf"):
            p = project/rel
            if p.exists():
                roots.append(p)

        findings = []
        files = 0
        for root in roots:
            for p in root.rglob("*.py"):
                files += 1
                try:
                    tree = ast.parse(p.read_text(encoding="utf-8"))
                except Exception as exc:
                    findings.append(BoundaryFinding(
                        str(p.relative_to(project)), 0, "PARSE_FAILURE", str(exc)
                    ))
                    continue
                rel = str(p.relative_to(project))
                is_rsf = "/rsf/" in f"/{rel}/" or "/reliability/" in f"/{rel}/"
                is_raf = "/raf/" in f"/{rel}/" or "/release/" in f"/{rel}/"

                for node in ast.walk(tree):
                    if is_rsf and isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if node.name in cls.RSF_FORBIDDEN_CALLS:
                            findings.append(BoundaryFinding(rel, node.lineno, "RSF_RELEASE_AUTHORITY_LEAK", node.name))
                    if is_raf and isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                        if any(name in node.name for name in cls.RAF_FORBIDDEN_NAMES):
                            findings.append(BoundaryFinding(rel, node.lineno, "RAF_RELIABILITY_AUTHORITY_LEAK", node.name))

                    # hardcoded terminal assurance truth is prohibited in boundary modules
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id.lower() in {
                                "certified","all_checks_passed","boundary_clean","assurance_pass"
                            }:
                                if isinstance(node.value, ast.Constant) and node.value.value is True:
                                    findings.append(BoundaryFinding(
                                        rel, node.lineno, "HARDCODED_PASS_STATE", target.id
                                    ))
        return BoundaryCertificationResult(not findings, files, tuple(findings))
