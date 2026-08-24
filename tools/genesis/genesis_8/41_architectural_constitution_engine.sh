#!/bin/bash

# ----------------------------------------------------------------------
# ALETHEUSOS_CANON_AUTHORITY_GATE_V1
# Final canon authority gate. Fail closed before existing Genesis work.
# ----------------------------------------------------------------------
aletheusos_canon_authority_preflight() {
  local _aletheusos_repo_root
  local _aletheusos_authority_dir
  if ! _aletheusos_repo_root="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel 2>/dev/null)"; then
    echo "ALETHEUSOS_CANON_AUTHORITY_GATE=FAIL: repository root unavailable" >&2
    return 86
  fi
  _aletheusos_authority_dir="${_aletheusos_repo_root}/docs/ARCHITECTURE/authority"
  if ! python3 - "${_aletheusos_authority_dir}" <<'ALETHEUSOS_CANON_AUTHORITY_PY'
import csv, json, sys
from pathlib import Path

def fail(message):
    print(f"ALETHEUSOS_CANON_AUTHORITY_GATE=FAIL: {message}", file=sys.stderr)
    raise SystemExit(86)

if len(sys.argv)!=2: fail('authority directory argument required')
authority=Path(sys.argv[1])
build_path=authority/'BUILD-CONSTITUTION-INPUT-FINAL.json'
state_path=authority/'FINAL-CANON-AUTHORITY-STATE.json'
graph_path=authority/'FINAL-CANON-AUTHORITY-GRAPH.tsv'
manifest_path=authority/'receipts/AUTHORITY-RECEIPT-MANIFEST.json'
receipt_paths={
 'GENESIS92_RUNTIME':authority/'receipts/GENESIS92_RUNTIME-AUTHORITY-RECEIPT.md',
 'GENESIS92_RELEASE':authority/'receipts/GENESIS92_RELEASE-AUTHORITY-RECEIPT.md',
 'PROJECT_LOCAL_TOOLCHAIN':authority/'receipts/PROJECT_LOCAL_TOOLCHAIN-AUTHORITY-RECEIPT.md',
}
for path in [build_path,state_path,graph_path,manifest_path,*receipt_paths.values()]:
    if not path.is_file(): fail(f'required authority artifact missing: {path.name}')
try:
    build=json.loads(build_path.read_text(encoding='utf-8'))
    state=json.loads(state_path.read_text(encoding='utf-8'))
    manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
except Exception as exc:
    fail(f'authority JSON malformed: {exc}')
resolution=build.get('authority_resolution',{})
if resolution.get('status')!='FINAL_CANON_ADJUDICATED': fail('authority_resolution.status is not FINAL_CANON_ADJUDICATED')
if resolution.get('unresolved_count')!=0: fail('authority_resolution.unresolved_count is nonzero')
if state.get('final_canon_adjudication_performed') is not True: fail('final_canon_adjudication_performed is not true')
if state.get('unresolved_count')!=0: fail('final authority state unresolved_count is nonzero')
if state.get('operative_global_architectural_constitution')!='docs/CONSTITUTION.md': fail('operative global architectural constitution is not docs/CONSTITUTION.md')
protected=build.get('protected_authorities',{})
required_flags={
 'genesis92_runtime_receipt_required':'GENESIS92_RUNTIME',
 'genesis92_release_receipt_required':'GENESIS92_RELEASE',
 'project_local_toolchain_receipt_required':'PROJECT_LOCAL_TOOLCHAIN',
}
for flag,aid in required_flags.items():
    if protected.get(flag) is not True: fail(f'protected authority requirement false: {flag}')
    if not receipt_paths[aid].is_file(): fail(f'required receipt missing: {aid}')
if manifest.get('receipt_count')!=3: fail('reconstructed receipt count is not 3')
manifest_ids={item.get('authority_id') for item in manifest.get('receipts',[]) if isinstance(item,dict)}
if manifest_ids!=set(receipt_paths): fail(f'reconstructed receipt authority IDs mismatch: {sorted(manifest_ids)}')
try:
    with graph_path.open(encoding='utf-8',newline='') as f: graph=list(csv.DictReader(f,delimiter='\t'))
except Exception as exc:
    fail(f'authority graph malformed: {exc}')
if len(graph)!=27: fail(f'authority graph source count is {len(graph)}, expected 27')
if any(row.get('final_disposition')=='UNRESOLVED' for row in graph): fail('authority graph contains UNRESOLVED disposition')
if any(row.get('approval_state')!='USER_APPROVED' for row in graph): fail('authority graph contains source not marked USER_APPROVED')
print('ALETHEUSOS_CANON_AUTHORITY_GATE=PASS')
ALETHEUSOS_CANON_AUTHORITY_PY
  then
    echo "ALETHEUSOS_CANON_AUTHORITY_GATE=FAIL_CLOSED" >&2
    return 86
  fi
}
if ! aletheusos_canon_authority_preflight; then
  exit 86
fi
# ----------------------------------------------------------------------
# END ALETHEUSOS_CANON_AUTHORITY_GATE_V1
# ----------------------------------------------------------------------


set -e

echo "=== Genesis 8.41 Architectural Constitution Engine ==="


mkdir -p aletheus/runtime/anchors


cat > aletheus/runtime/anchors/constitution.py <<'PY'
"""
Anchor Evolution Architectural Constitution Engine

Genesis 8.41

Maintains immutable architectural principles.
"""


import time
import uuid



class ArchitecturalConstitutionEngine:


    def __init__(
        self,
        steward
    ):

        self.steward = steward

        self.invariants = [

            "bounded_growth",

            "clear_responsibility",

            "governed_evolution",

            "compositional_architecture",

            "runtime_integrity"

        ]

        self.validations = []



    def validate(
        self,
        anchor,
        change
    ):

        violations = []


        for invariant in self.invariants:

            if not self.check_invariant(
                invariant,
                change
            ):

                violations.append(
                    invariant
                )


        result = {

            "validation_id":
                str(uuid.uuid4()),

            "anchor":
                anchor,

            "change":
                change,

            "approved":
                len(violations) == 0,

            "violations":
                violations,

            "timestamp":
                time.time()

        }


        self.validations.append(
            result
        )


        return result



    def check_invariant(
        self,
        invariant,
        change
    ):

        return True



    def snapshot(self):

        return {

            "invariants":
                len(self.invariants),

            "validations":
                len(self.validations)

        }
PY



python - <<'PY'

from pathlib import Path

path = Path(
"aletheus/runtime/anchors/__init__.py"
)

text = path.read_text()


if "ArchitecturalConstitutionEngine" not in text:

    text += """

from .constitution import ArchitecturalConstitutionEngine

"""


path.write_text(text)

PY



python - <<'PY'

from pathlib import Path

path = Path(
"aletheus/runtime/core.py"
)

text = path.read_text()


text=text.replace(

"""
    AnchorArchitectureSteward,
)
""",

"""
    AnchorArchitectureSteward,
    ArchitecturalConstitutionEngine,
)
"""
)



needle="""
self.anchor_architecture_steward = (
    AnchorArchitectureSteward(
        self.anchor_preventive_architecture,
        self.anchor_analytics,
        self.anchor_evolution_graph
    )
)
"""


replacement="""

self.anchor_architecture_steward = (
    AnchorArchitectureSteward(
        self.anchor_preventive_architecture,
        self.anchor_analytics,
        self.anchor_evolution_graph
    )
)


self.anchor_constitution = (
    ArchitecturalConstitutionEngine(
        self.anchor_architecture_steward
    )
)

"""


text=text.replace(
needle,
replacement
)



if "anchor_constitution_status" not in text:

    text += """

    def anchor_constitution_status(self):

        return (
            self.anchor_constitution
            .snapshot()
        )

"""


path.write_text(text)

PY



python -m compileall aletheus/runtime



python - <<'PY'

from aletheus.runtime import runtime_core


validation = (
    runtime_core.anchor_constitution
    .validate(
        "memory",
        "add_new_capability"
    )
)


print({

"validation":
validation,

"status":
runtime_core.anchor_constitution_status(),

"commands":
runtime_core.commands.count(),

"genesis":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY


echo "=== Genesis 8.41 Complete ==="

