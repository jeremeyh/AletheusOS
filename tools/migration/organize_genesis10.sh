#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(pwd)"
WORK="${ROOT}/Genesis10_Work_Organization"

echo
echo "======================================================"
echo " Genesis 10 Work Organizer"
echo "======================================================"
echo

mkdir -p \
    "${WORK}/01_repository_intelligence/tools" \
    "${WORK}/01_repository_intelligence/tests" \
    "${WORK}/01_repository_intelligence/docs" \
    "${WORK}/02_runtime_architecture/docs" \
    "${WORK}/03_platform_updates" \
    "${WORK}/04_reports" \
    "${WORK}/05_history" \
    "${WORK}/06_release_artifacts" \
    "${WORK}/07_misc"

copy_if_exists () {
    local SRC="$1"
    local DST="$2"

    if [[ -e "$SRC" ]]; then
        echo "✓ $SRC"
        cp -R "$SRC" "$DST"
    else
        echo "• Missing: $SRC"
    fi
}

###############################################################################
# Repository Intelligence
###############################################################################

copy_if_exists tools/repository                         "${WORK}/01_repository_intelligence/tools/"
copy_if_exists tools/doctor                             "${WORK}/01_repository_intelligence/tools/"
copy_if_exists tools/migration/genesis10_repository_normalization.py \
               "${WORK}/01_repository_intelligence/tools/"

copy_if_exists tests/architecture \
               "${WORK}/01_repository_intelligence/tests/"

###############################################################################
# Runtime Architecture
###############################################################################

for f in \
    docs/ARCHITECTURE/crk_constitutional_ownership_map.md \
    docs/ARCHITECTURE/crk_constitutional_ownership_map.json \
    docs/ARCHITECTURE/runtime_core_decomposition_baseline.md \
    docs/ARCHITECTURE/runtime_v5_command_inventory.txt \
    docs/ARCHITECTURE/release_cleanup_report.md \
    docs/ARCHITECTURE_IDENTITY.md
do
    copy_if_exists "$f" "${WORK}/02_runtime_architecture/docs/"
done

###############################################################################
# Platform
###############################################################################

copy_if_exists AletheusOS_Genesis10_Updates \
               "${WORK}/03_platform_updates/"

copy_if_exists aletheus/version.py \
               "${WORK}/03_platform_updates/"

###############################################################################
# Reports
###############################################################################

mkdir -p "${WORK}/04_reports"

for d in reports/*; do
    [[ -e "$d" ]] || continue
    copy_if_exists "$d" "${WORK}/04_reports/"
done

copy_if_exists nimble/reports \
               "${WORK}/04_reports/"

copy_if_exists aletheus/card_hawk/reports \
               "${WORK}/04_reports/"

copy_if_exists aletheus/intelligence/reports \
               "${WORK}/04_reports/"

###############################################################################
# History
###############################################################################

copy_if_exists history \
               "${WORK}/05_history/"

###############################################################################
# Release Artifacts
###############################################################################

copy_if_exists AletheusOS_Repository_Self_Repair_SHA256.txt \
               "${WORK}/06_release_artifacts/"

###############################################################################
# Misc
###############################################################################

copy_if_exists clean_diff.txt \
               "${WORK}/07_misc/"

copy_if_exists repo_diff.txt \
               "${WORK}/07_misc/"

###############################################################################
# Inventory
###############################################################################

find "${WORK}" -type f | sort > "${WORK}/inventory.txt"

cat > "${WORK}/README.md" <<'EOF'
Genesis 10 Work Organization

01_repository_intelligence
    Repository tooling, diagnostics, normalization

02_runtime_architecture
    Runtime architecture, CRK, ownership, identity

03_platform_updates
    Genesis 10 implementation work

04_reports
    Generated reports and audits

05_history
    Historical artifacts

06_release_artifacts
    Checksums and release metadata

07_misc
    Temporary investigation artifacts

inventory.txt
    Complete file inventory
EOF

echo
echo "======================================================"
echo "Organization Complete"
echo "======================================================"
echo
echo "Workspace:"
echo "  ${WORK}"
echo
