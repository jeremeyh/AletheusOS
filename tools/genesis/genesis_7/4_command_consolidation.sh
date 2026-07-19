#!/bin/bash

set -e

echo "=== Genesis 7.4 Command Registration Consolidation ==="


cp aletheus/runtime/core.py \
aletheus/runtime/core.py.genesis7_4_backup


mkdir -p aletheus/runtime/managers



cat > aletheus/runtime/managers/command_manager.py <<'PY'
"""
Command Manager

Genesis 7.4

Canonical command surface authority.
"""

from aletheus.runtime.command_bootstrap.bootstrapper import (
    RuntimeCommandBootstrapper
)


class CommandManager:

    def __init__(self, runtime):

        self.runtime = runtime
        self.bootstrapper = RuntimeCommandBootstrapper()


    def bootstrap(self):

        self.bootstrapper.bootstrap(
            self.runtime
        )

        return self.status()


    def count(self):

        return self.runtime.commands.count()


    def list(self):

        return self.runtime.commands.list()


    def status(self):

        return {

            "registered":
                self.count(),

            "bootstrapper":
                type(self.bootstrapper).__name__,

            "healthy":
                self.count() > 0
        }
PY



python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/core.py"
)

text = path.read_text()


# Remove old registration imports

start = text.find(
"from aletheus.runtime.registrations import"
)


if start != -1:

    end = text.find(
        ")",
        start
    )

    text = (
        text[:start]
        +
        text[end+1:]
    )



# Add bootstrap import

marker = (
"from aletheus.runtime.integrity "
"import RuntimeInvariantEngine, RuntimeBootValidator"
)


addition = """

from aletheus.runtime.command_bootstrap.bootstrapper import (
    RuntimeCommandBootstrapper
)

"""


if "RuntimeCommandBootstrapper" not in text:

    text=text.replace(
        marker,
        marker + addition
    )


# Replace command initialization section

text=text.replace(

"self.commands = CommandBus(self)",

"""
self.commands = CommandBus(self)

self.command_bootstrapper = (
    RuntimeCommandBootstrapper()
)
"""

)



path.write_text(text)

PY




python - <<'PY'

from pathlib import Path
import re


path=Path(
"aletheus/runtime/core.py"
)


text=path.read_text()


# Add command bootstrap into boot()

needle="""
    def boot(self) -> None:
"""


if needle in text:

    replacement="""
    def boot(self) -> None:
"""

    text=text.replace(
        needle,
        replacement
    )


# Ensure bootstrap occurs once

if "self.command_bootstrapper.bootstrap(self)" not in text:

    text=text.replace(

        "def boot(self) -> None:\n",

        "def boot(self) -> None:\n\n        self.command_bootstrapper.bootstrap(self)\n"

    )


path.write_text(text)

PY




python -m compileall aletheus/runtime



python - <<'PY'

from aletheus.runtime import runtime_core


print({

"commands":
runtime_core.commands.count(),

"command_status":
runtime_core.command_manager.status(),

"genesis6":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY



echo "=== Genesis 7.4 Complete ==="

