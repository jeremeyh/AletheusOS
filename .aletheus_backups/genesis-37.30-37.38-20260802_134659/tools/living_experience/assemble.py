import argparse
import hashlib
import json
import shutil
from pathlib import Path


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    x = argparse.ArgumentParser()
    x.add_argument("--template", type=Path, required=True)
    x.add_argument("--wasm", type=Path, required=True)
    x.add_argument("--web", type=Path, required=True)
    x.add_argument("--out", type=Path, required=True)
    a = x.parse_args()
    if a.out.exists():
        shutil.rmtree(a.out)
    shutil.copytree(a.template, a.out)
    for crate, dest in {
        "living_physics_core": "core/physics",
        "resonance_field_core": "core/resonance",
        "ambient_elasticity_core": "core/elasticity",
    }.items():
        target = a.out / dest
        target.mkdir(parents=True, exist_ok=True)
        for f in (a.wasm / crate).glob("*"):
            if f.is_file():
                shutil.copy2(f, target / f.name)
    if a.web.exists():
        shutil.copytree(a.web, a.out / "web", dirs_exist_ok=True)
    files = [
        f for f in a.out.rglob("*") if f.is_file() and f.name != "checksums.sha256"
    ]
    c = a.out / "manifests/checksums.sha256"
    c.parent.mkdir(parents=True, exist_ok=True)
    c.write_text(
        "\n".join(f"{sha(f)}  {f.relative_to(a.out)}" for f in sorted(files)) + "\n"
    )
    m = json.loads((a.out / "manifest.json").read_text())
    m["artifactState"] = "compiled"
    (a.out / "manifest.json").write_text(json.dumps(m, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
