from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--template", type=Path, required=True)
    p.add_argument("--wasm-root", type=Path, required=True)
    p.add_argument("--web-dist", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    if args.out.exists():
        shutil.rmtree(args.out)
    shutil.copytree(args.template, args.out)

    mapping = {
        "info_physics_core": "core/physics",
        "axiomux_renderer": "core/renderer",
        "hyperbolic_engine": "core/navigation",
        "telemetry_core": "core/telemetry",
    }
    for crate, dest_rel in mapping.items():
        source = args.wasm_root / crate
        dest = args.out / dest_rel
        dest.mkdir(parents=True, exist_ok=True)
        if source.exists():
            for file in source.iterdir():
                if file.is_file():
                    shutil.copy2(file, dest / file.name)

    if args.web_dist.exists():
        shutil.copytree(args.web_dist, args.out / "web", dirs_exist_ok=True)

    files = [
        p for p in args.out.rglob("*") if p.is_file() and p.name != "checksums.sha256"
    ]
    checksum = args.out / "manifests" / "checksums.sha256"
    checksum.parent.mkdir(parents=True, exist_ok=True)
    checksum.write_text(
        "\n".join(f"{sha256(f)}  {f.relative_to(args.out)}" for f in sorted(files))
        + "\n"
    )
    manifest = json.loads((args.out / "manifest.json").read_text())
    manifest["artifactState"] = (
        "compiled"
        if all(
            (args.out / path).exists()
            for path in [
                "core/physics/info_physics_core_bg.wasm",
                "core/renderer/axiomux_renderer_bg.wasm",
                "core/navigation/hyperbolic_engine_bg.wasm",
                "core/telemetry/telemetry_core_bg.wasm",
            ]
        )
        else "partially-compiled"
    )
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
