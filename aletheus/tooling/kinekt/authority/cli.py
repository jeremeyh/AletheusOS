import argparse
from pathlib import Path

from .engine import AuthorityEngine


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "command", choices=("analyze", "validate"), nargs="?", default="analyze"
    )
    p.add_argument(
        "--registry",
        type=Path,
        default=Path("config/kinekt/capability_authorities.json"),
    )
    p.add_argument(
        "--twin",
        type=Path,
        default=Path(
            "reports/architecture/kinekt/twin/architectural-digital-twin.json"
        ),
    )
    p.add_argument(
        "--output", type=Path, default=Path("reports/architecture/kinekt/authority")
    )
    a = p.parse_args()
    r = AuthorityEngine(a.registry, a.twin, a.output).analyze()
    critical = sum(f.severity == "critical" for f in r.findings)
    print(
        f"Capability authority analysis complete: {len(r.capabilities)} capabilities, {len(r.module_assignments)} assigned modules, {len(r.unresolved_modules)} unresolved modules, {critical} critical overlaps."
    )
    print(f"Reports: {a.output.resolve()}")
    return 1 if a.command == "validate" and critical else 0
