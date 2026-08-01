from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/process_grid_consolidation"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        {
            "Semantic Rail Continuity Gate": root
            / "semantic_rail_gate/semantic-rail-continuity-gate.json",
            "Full Platform Continuity Gate": root
            / "platform_continuity/full-platform-continuity-gate.json",
            "Vertical Slice Verifier": root
            / "vertical_slice_verification/vertical-slice-verification.json",
            "Horizontal Mesh Verifier": root
            / "horizontal_mesh_verification/horizontal-mesh-verification.json",
            "Runtime Diagnostics": root
            / "runtime_diagnostics/constitutional-runtime-diagnostics.json",
            "Runtime Observability": root
            / "runtime_observability/runtime-observability.json",
            "Runtime Telemetry": root / "runtime_telemetry/runtime-telemetry.json",
            "Architectural Governance": root / "governance/governance-findings.json",
        },
        args.output,
    ).build()
    print(
        "Process Grid Consolidation complete: "
        f"absorbed={report['absorbed_components']}, "
        f"functionality_removed={report['functionality_removed']}."
    )
    return 0
