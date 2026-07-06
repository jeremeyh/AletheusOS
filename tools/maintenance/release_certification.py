from __future__ import annotations

import json
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

REPORT_DIR = ROOT / "reports" / "release_certification"
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def run_command(command: list[str]) -> dict:
    result = subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    return {
        "command": " ".join(command),
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "passed": result.returncode == 0,
    }


def main():
    from aletheus.runtime import runtime_core
    from aletheus.kernel import kernel
    from aletheus.discovery import DiscoveryEngine

    runtime_core.boot()

    discovery = DiscoveryEngine(ROOT / "aletheus")
    discovered = discovery.discover()

    runtime_census = run_command(
        ["python3", "tools/maintenance/runtime_census.py"]
    )

    platform_inspection = run_command(
        ["python3", "tools/maintenance/platform_inspection.py"]
    )

    checks = {
        "runtime_census": runtime_census["passed"],
        "platform_inspection": platform_inspection["passed"],
        "kernel_online": kernel.stats().get("status") == "online",
        "runtime_online": runtime_core.status == "online",
        "discovery_loaded": all(item.get("loaded") for item in discovered),
    }

    certified = all(checks.values())

    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "platform": "AletheusOS",
        "certified": certified,
        "checks": checks,
        "kernel": kernel.stats(),
        "runtime": {
            "version": runtime_core.version,
            "status": runtime_core.status,
            "commands": runtime_core.commands.count(),
            "services": runtime_core.services.count(),
        },
        "discovery": {
            "discovered": len(discovered),
            "loaded": sum(1 for item in discovered if item.get("loaded")),
        },
        "commands": {
            "runtime_census": runtime_census,
            "platform_inspection": platform_inspection,
        },
    }

    json_file = REPORT_DIR / "release_certification.json"
    md_file = REPORT_DIR / "release_certification.md"

    json_file.write_text(json.dumps(report, indent=2), encoding="utf-8")

    md_file.write_text(
        "\n".join(
            [
                "# AletheusOS Release Certification",
                "",
                f"Generated: {report['generated_at']}",
                "",
                "## Decision",
                "",
                f"- Certified: **{report['certified']}**",
                "",
                "## Checks",
                "",
                *[
                    f"- {name}: {'PASS' if passed else 'FAIL'}"
                    for name, passed in checks.items()
                ],
                "",
                "## Runtime",
                "",
                f"- Version: {report['runtime']['version']}",
                f"- Status: {report['runtime']['status']}",
                f"- Commands: {report['runtime']['commands']}",
                f"- Services: {report['runtime']['services']}",
                "",
                "## Kernel",
                "",
                f"- Version: {report['kernel'].get('version')}",
                f"- Status: {report['kernel'].get('status')}",
                "",
                "## Discovery",
                "",
                f"- Discovered: {report['discovery']['discovered']}",
                f"- Loaded: {report['discovery']['loaded']}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print("AletheusOS Release Certification")
    print("=" * 40)
    print(f"Certified: {certified}")
    print(f"JSON: {json_file}")
    print(f"MD:   {md_file}")

    raise SystemExit(0 if certified else 1)


if __name__ == "__main__":
    main()
