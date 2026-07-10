#!/usr/bin/env bash
set -e

mkdir -p reports/genesis_7_architecture_audit/backups/final_command_repair

if [ -f aletheus/runtime/commands.py ]; then
    mv \
        aletheus/runtime/commands.py \
        reports/genesis_7_architecture_audit/backups/final_command_repair/legacy_runtime_commands_module.py

    echo "Moved legacy commands.py into backup."
else
    echo "No legacy commands.py found."
fi
