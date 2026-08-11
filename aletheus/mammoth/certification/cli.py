import argparse
from datetime import datetime, timezone
from .engine import MammothProjectLevelCertificationEngine

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--project-root",required=True)
    p.add_argument("--output-directory",required=True)
    p.add_argument("--closure-evidence")
    a=p.parse_args()
    r=MammothProjectLevelCertificationEngine.certify(
        project_root=a.project_root, output_directory=a.output_directory,
        closure_evidence=a.closure_evidence,
        inspected_at_iso=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    )
    print("="*78)
    print(" ALETHEUSOS RAF/RSF — MAMMOTH PROJECT-LEVEL CERTIFICATION")
    print("="*78)
    for c in r.checks:
        print(f"{c.check_id}: {'PASS' if c.passed else 'FAIL'}")
        for v in c.violations[:20]: print("  -",v)
        if len(c.violations)>20: print(f"  ... {len(c.violations)-20} more")
    print("STATUS:",r.status)
    print("CERTIFICATION_DIGEST:",r.certification_digest)
    print("="*78)
    return 0 if r.status=="CERTIFIED" else 3

if __name__=="__main__": raise SystemExit(main())
