from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

CRATES = (
    "info_physics_core",
    "axiomux_renderer",
    "hyperbolic_engine",
    "telemetry_core",
)


def run(cmd: list[str], cwd: Path) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--rust-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    if not shutil.which("cargo"):
        raise SystemExit("cargo unavailable")
    if not shutil.which("wasm-pack"):
        raise SystemExit("wasm-pack unavailable")
    for crate in CRATES:
        crate_dir = args.rust_root / crate
        run(
            [
                "wasm-pack",
                "build",
                str(crate_dir),
                "--target",
                "web",
                "--release",
                "--out-dir",
                str(args.out / crate),
            ],
            args.rust_root,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
