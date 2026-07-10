#!/bin/bash

set -e

echo "=== Genesis 7.3 Core Delegation ==="


cp aletheus/runtime/core.py \
aletheus/runtime/core.py.genesis7_3_backup


python - <<'PY'
from pathlib import Path
import re


path = Path(
"aletheus/runtime/core.py"
)

text = path.read_text()


def replace_method(name, body):

    global text

    pattern = (
        r"\n    def "
        + name
        + r"\(.*?(?=\n    def |\n$)"
    )

    text = re.sub(
        pattern,
        "\n" + body,
        text,
        flags=re.S
    )



replace_method(
"health",
'''
    def health(self):
        """
        Runtime health contract.

        Delegated to HealthManager.
        Genesis 7.3
        """

        return self.health_manager.health()
'''
)



replace_method(
"registry_snapshot",
'''
    def registry_snapshot(self):

        """
        Registry snapshot contract.

        Delegated to RegistryManager.
        """

        return self.registry_manager.snapshot()
'''
)



replace_method(
"command_surface_audit",
'''
    def command_surface_audit(self):

        """
        Command inventory contract.

        Delegated to CommandManager.
        """

        return {
            "count":
                self.command_manager.count(),

            "commands":
                self.command_manager.list()
        }
'''
)



replace_method(
"boot_certification_validate",
'''
    def boot_certification_validate(self):

        """
        Boot certification contract.

        Delegated to ValidationManager.
        """

        return self.validation_manager.boot_certification()
'''
)



replace_method(
"genesis6_validate",
'''
    def genesis6_validate(self):

        """
        Genesis validation contract.

        Delegated to ValidationManager.
        """

        return self.validation_manager.genesis6_validate()
'''
)



path.write_text(text)

PY



echo "Compile"

python -m compileall aletheus/runtime



echo "Runtime validation"


python - <<'PY'

from aletheus.runtime import runtime_core


print({

"commands":
runtime_core.commands.count(),

"health":
runtime_core.health(),

"registry":
runtime_core.registry_snapshot().get(
"version"
),

"cert":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY



echo "=== Genesis 7.3 Complete ==="

