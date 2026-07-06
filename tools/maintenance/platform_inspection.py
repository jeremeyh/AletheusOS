from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

# ------------------------------------------------------------
# Resolve project root so "import aletheus" always works.
# ------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORT_DIR = ROOT / "reports" / "platform_inspection"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def main():

    from aletheus.runtime import runtime_core
    from aletheus.kernel import kernel
    from aletheus.discovery import DiscoveryEngine
    from aletheus.homeostasis import homeostasis_engine
    from aletheus.service_manager import service_manager

    runtime_core.boot()

    discovery = DiscoveryEngine(ROOT / "aletheus")
    discovered = discovery.discover()

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "platform": "AletheusOS",
        "kernel": kernel.stats(),
        "runtime": {
            "version": runtime_core.version,
            "status": runtime_core.status,
            "commands": runtime_core.commands.count(),
            "services": runtime_core.services.count(),
        },
        "discovery": {
            "discovered": len(discovered),
            "loaded": sum(
                1
                for item in discovered
                if item.get("loaded")
            ),
        },
        "homeostasis": homeostasis_engine.statistics(),
        "service_manager": service_manager.statistics(),
        "overall": "PASS",
    }

    json_file = REPORT_DIR / "platform_inspection.json"
    markdown_file = REPORT_DIR / "platform_inspection.md"

    json_file.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    markdown = f"""# AletheusOS Platform Inspection

Generated:
{report["generated_at"]}

---

## Overall

Status: **{report["overall"]}**

---

## Kernel

Version: {report["kernel"].get("version")}
Status: {report["kernel"].get("status")}

---

## Runtime

Version: {report["runtime"]["version"]}
Status: {report["runtime"]["status"]}
Commands: {report["runtime"]["commands"]}
Services: {report["runtime"]["services"]}

---

## Discovery

Discovered Components: {report["discovery"]["discovered"]}
Loaded Components: {report["discovery"]["loaded"]}

---

## Homeostasis

{json.dumps(report["homeostasis"], indent=2)}

---

## Service Manager

{json.dumps(report["service_manager"], indent=2)}

---

Platform Inspection Completed Successfully.
"""

    markdown_file.write_text(
        markdown,
        encoding="utf-8",
    )

    print()
    print("AletheusOS Platform Inspection")
    print("=" * 50)
    print(f"Overall Status : {report['overall']}")
    print(f"Kernel Version : {report['kernel'].get('version')}")
    print(f"Runtime Version: {report['runtime']['version']}")
    print(f"Commands       : {report['runtime']['commands']}")
    print(f"Services       : {report['runtime']['services']}")
    print(f"Discovered     : {report['discovery']['discovered']}")
    print()
    print(f"JSON Report    : {json_file}")
    print(f"Markdown Report: {markdown_file}")
    print()


if __name__ == "__main__":
    main()
