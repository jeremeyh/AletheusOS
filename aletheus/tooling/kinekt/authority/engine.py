from datetime import UTC, datetime
from pathlib import Path

from .analysis import assign_modules, detect_claim_overlaps, parse_authorities
from .loader import load_object
from .models import AuthorityReport
from .reporting import write_reports


class AuthorityEngine:
    def __init__(self, registry_path: Path, twin_path: Path, output: Path):
        self.registry_path = registry_path.resolve()
        self.twin_path = twin_path.resolve()
        self.output = output.resolve()

    def analyze(self) -> AuthorityReport:
        authorities = parse_authorities(load_object(self.registry_path))
        assignments, unresolved, af = assign_modules(
            load_object(self.twin_path), authorities
        )
        findings = detect_claim_overlaps(authorities) + af
        report = AuthorityReport(
            datetime.now(UTC).isoformat(),
            str(self.registry_path),
            str(self.twin_path),
            authorities,
            assignments,
            findings,
            unresolved,
        )
        write_reports(report, self.output)
        return report
