import argparse
import subprocess
from pathlib import Path

CRATES = ("living_physics_core", "resonance_field_core", "ambient_elasticity_core")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--rust-root", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args()
    root = a.rust_root.resolve()
    a.out.mkdir(parents=True, exist_ok=True)
    for crate in CRATES:
        subprocess.run(
            [
                "wasm-pack",
                "build",
                str(root / crate),
                "--target",
                "web",
                "--release",
                "--out-dir",
                str(a.out / crate),
            ],
            cwd=root,
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
