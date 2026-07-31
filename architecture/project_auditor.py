from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class AuditFinding:
    file: str
    issue: str
    detail: str


@dataclass
class ProjectAuditReport:
    findings: list[AuditFinding] = field(default_factory=list)

    def add(self, file, issue, detail):
        self.findings.append(AuditFinding(str(file), issue, detail))

    def to_dict(self):
        return [finding.__dict__ for finding in self.findings]

    def summary(self):
        counts = {}
        for finding in self.findings:
            counts[finding.issue] = counts.get(finding.issue, 0) + 1
        return counts


class ProjectAuditor:
    """
    CardHawk OS™ Project Auditor

    Scans for architectural drift, deprecated imports, duplicate package usage,
    and likely consolidation issues.
    """

    DEPRECATED_PATTERNS = {
        "deprecated_engine_package": ["from engine", "import engine"],
        "deprecated_cardhawk_aeye_package": [
            "from cardhawk_aeye",
            "import cardhawk_aeye",
        ],
        "legacy_hawk_a_eye_spelling": ["hawk_a_eye"],
    }

    @staticmethod
    def audit(root="."):
        root = Path(root)
        report = ProjectAuditReport()

        for path in root.rglob("*.py"):
            if any(part in {".venv", "venv", "__pycache__"} for part in path.parts):
                continue

            text = path.read_text(errors="ignore")

            for issue, patterns in ProjectAuditor.DEPRECATED_PATTERNS.items():
                for pattern in patterns:
                    if pattern in text:
                        report.add(path, issue, f"Found pattern: {pattern}")

        if (root / "engine").exists() and (root / "engines").exists():
            report.add(
                "project_root",
                "duplicate_engine_folders",
                "Both engine/ and engines/ exist. Canonical package is engines/.",
            )

        if (root / "cardhawk_aeye").exists() and (root / "hawk_aeye").exists():
            report.add(
                "project_root",
                "duplicate_aeye_folders",
                "Both cardhawk_aeye/ and hawk_aeye/ exist. Canonical package is hawk_aeye/.",
            )

        return report
