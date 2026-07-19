#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="Genesis10_Work_Organization"

echo
echo "=============================="
echo " Genesis 10 Inventory Summary"
echo "=============================="
echo

for d in "$ROOT"/*; do
    [[ -d "$d" ]] || continue

    files=$(find "$d" -type f | wc -l | tr -d ' ')
    dirs=$(find "$d" -type d | wc -l | tr -d ' ')
    size=$(du -sh "$d" | awk '{print $1}')

    printf "%-35s %6s files %6s dirs %8s\n" \
        "$(basename "$d")" \
        "$files" \
        "$dirs" \
        "$size"
done

echo
echo "Largest directories:"
du -sh "$ROOT"/* | sort -h
