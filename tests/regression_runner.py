from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TESTS = [
    ("v3.7 Security", "tests/test_aletheus_v37_security.py"),
    ("v3.9 Tenancy", "tests/test_aletheus_v39_tenancy.py"),
    ("v4.0 Kernel", "tests/test_aletheus_v40_kernel.py"),
    ("v4.1 Compatibility", "tests/test_aletheus_v41_compatibility.py"),
]

def main():
    print("=" * 70)
    print("AletheusOS Regression Suite")
    print("=" * 70)

    passed = 0

    for name, path in TESTS:
        print(f"\nRunning {name}...")
        result = subprocess.run(
            [sys.executable, path],
            cwd=Path(__file__).resolve().parents[1],
        )

        if result.returncode == 0:
            print(f"✓ {name}")
            passed += 1
        else:
            print(f"✗ {name}")
            raise SystemExit(result.returncode)

    print("\n" + "=" * 70)
    print(f"Result: {passed}/{len(TESTS)} Passed")
    print("Runtime Healthy")
    print("=" * 70)

if __name__ == "__main__":
    main()
