#!/usr/bin/env python3
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[2]

def run(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name:<18} {detail}")

def main():
    run("Repository", (ROOT/"docs").exists() and (ROOT/"tools").exists())
    run("Runtime", (ROOT/"aletheus/runtime/core.py").exists())
    run("Architecture", (ROOT/"tests/architecture").exists())
    ver=(ROOT/"aletheus/version.py").exists()
    run("Versions", ver)
    try:
        p=subprocess.run(["git","status","--porcelain"],cwd=ROOT,capture_output=True,text=True)
        run("Git", p.returncode==0, "clean" if p.stdout.strip()=="" else "changes present")
    except Exception as e:
        run("Git",False,str(e))
    return 0
if __name__=="__main__":
    raise SystemExit(main())
