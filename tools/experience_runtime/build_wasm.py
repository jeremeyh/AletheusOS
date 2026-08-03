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
    """Run a build command from the supplied working directory."""
    print()
    print(f"Working directory: {cwd}")
    print(f"Command: {' '.join(cmd)}")

    subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compile the Genesis 37 Rust runtimes with wasm-pack."
    )
    parser.add_argument(
        "--rust-root",
        type=Path,
        required=True,
        help="Path to the Rust workspace root.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Directory where compiled WASM packages will be written.",
    )
    args = parser.parse_args()

    rust_root = args.rust_root.expanduser().resolve()
    output_root = args.out.expanduser().resolve()

    if not shutil.which("cargo"):
        raise SystemExit("cargo unavailable")

    if not shutil.which("wasm-pack"):
        raise SystemExit("wasm-pack unavailable")

    workspace_manifest = rust_root / "Cargo.toml"
    if not workspace_manifest.is_file():
        raise SystemExit(
            f"Rust workspace Cargo.toml not found: {workspace_manifest}"
        )

    output_root.mkdir(parents=True, exist_ok=True)

    for crate in CRATES:
        crate_dir = rust_root / crate
        crate_manifest = crate_dir / "Cargo.toml"
        crate_output = output_root / crate

        print()
        print("=" * 72)
        print(f"Compiling WASM crate: {crate}")
        print(f"Crate directory: {crate_dir}")
        print(f"Cargo.toml exists: {crate_manifest.is_file()}")
        print(f"Output directory: {crate_output}")
        print("=" * 72)

        if not crate_dir.is_dir():
            raise SystemExit(f"Crate directory not found: {crate_dir}")

        if not crate_manifest.is_file():
            raise SystemExit(f"Crate Cargo.toml not found: {crate_manifest}")

        crate_output.mkdir(parents=True, exist_ok=True)

        run(
            [
                "wasm-pack",
                "build",
                str(crate_dir),
                "--target",
                "web",
                "--release",
                "--out-dir",
                str(crate_output),
            ],
            cwd=rust_root,
        )

    print()
    print("=" * 72)
    print("All Genesis 37 WebAssembly crates compiled successfully.")
    print(f"Output root: {output_root}")
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
