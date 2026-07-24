#!/usr/bin/env bash
set -euo pipefail

mkdir -p bin

cat > bin/create_nimble_signed_audit_anchor.py <<'PY'
#!/usr/bin/env python3
"""
Executable wrapper for the Nimble signed audit anchor creator.
"""

from tools.create.create_nimble_signed_audit_anchor import main


if __name__ == "__main__":
    raise SystemExit(main())
PY

chmod +x bin/create_nimble_signed_audit_anchor.py

echo "✓ Created bin/create_nimble_signed_audit_anchor.py"
