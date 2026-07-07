#!/bin/bash
set -e

echo "== AletheusOS Genesis Layout Repair =="

mkdir -p engineering/genesis_packages
mkdir -p engineering/repository_dna
mkdir -p engineering/patches

# Known GP packages
for gp in GP-00029 GP-00030 GP-00031 GP-00032 GP-00033 GP-00034; do
  mkdir -p "engineering/genesis_packages/$gp"
done

echo "Moving accidental extracted GP folders out of aletheus/..."

for dir in aletheus/GP-*; do
  [ -d "$dir" ] || continue
  gp=$(basename "$dir" | cut -d_ -f1)
  mkdir -p "engineering/genesis_packages/$gp"

  find "$dir" -maxdepth 3 -type f \( \
    -name "*.md" -o \
    -name "manifest.yaml" -o \
    -name "*.patch" \
  \) -exec mv {} "engineering/genesis_packages/$gp/" \;

  rm -rf "$dir"
done

echo "Moving loose docs from package folders..."

for pkg in concept_collision_engine genesis atlas watch_tower oracle runtime_constitutional_integration; do
  case "$pkg" in
    concept_collision_engine) gp="GP-00029" ;;
    genesis) gp="GP-00030" ;;
    atlas) gp="GP-00031" ;;
    watch_tower) gp="GP-00032" ;;
    oracle) gp="GP-00033" ;;
    runtime_constitutional_integration) gp="GP-00034" ;;
  esac

  mkdir -p "engineering/genesis_packages/$gp"

  for file in \
    "aletheus/$pkg/README.md" \
    "aletheus/$pkg/ENGINEERING_NOTES.md" \
    "aletheus/$pkg/VERIFY.md" \
    "aletheus/$pkg/ROLLBACK.md" \
    "aletheus/$pkg/manifest.yaml" \
    "aletheus/$pkg/ADR-"*.md
  do
    [ -f "$file" ] && mv "$file" "engineering/genesis_packages/$gp/"
  done
done

echo "Removing accidental system artifacts..."
find aletheus -name ".DS_Store" -delete
find aletheus -name "*.zip" -delete

echo "Writing Repository DNA baseline..."
find aletheus -maxdepth 1 -type d | sort > engineering/repository_dna/subsystems.txt
find aletheus -name "*.py" | sort > engineering/repository_dna/python_files.txt
find aletheus -maxdepth 1 -type d | wc -l > engineering/repository_dna/top_level_subsystem_count.txt
find aletheus -name "*.py" | wc -l > engineering/repository_dna/python_file_count.txt

echo "Checking for remaining misplaced engineering docs in aletheus/..."
find aletheus -type f \( \
  -name "ENGINEERING_NOTES.md" -o \
  -name "VERIFY.md" -o \
  -name "ROLLBACK.md" -o \
  -name "manifest.yaml" -o \
  -name "ADR-*.md" \
\) | sort > engineering/repository_dna/misplaced_engineering_files.txt

echo
echo "== Done =="
echo "Review:"
echo "  engineering/repository_dna/misplaced_engineering_files.txt"
echo
