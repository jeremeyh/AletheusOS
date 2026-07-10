#!/usr/bin/env bash
set -e

echo
echo "Runtime command namespace:"
echo "=========================="

find aletheus/runtime \
    -maxdepth 2 \
    \( -name "commands.py" -o -name "commands" \) \
    -print

echo
echo "If only the following remains, the namespace collision is resolved:"
echo
echo "    aletheus/runtime/commands"
echo
echo "The file aletheus/runtime/boot/commands.py is expected and should remain."
