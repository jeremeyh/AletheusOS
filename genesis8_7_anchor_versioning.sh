#!/bin/bash

set -e

echo "=== Genesis 8.7 Anchor Versioning & Migration ==="


mkdir -p aletheus/runtime/anchors



cat > aletheus/runtime/anchors/versioning.py <<'PY'
"""
Anchor Version Manager

Genesis 8.7

Controls capability versions and migrations.
"""


import time



class AnchorVersionManager:


    def __init__(self, registry):

        self.registry = registry

        self.versions = {}

        self.migrations = {}

        self.history = []



    def register_version(
        self,
        anchor,
        version,
        metadata=None
    ):

        self.versions.setdefault(
            anchor,
            []
        )

        if version not in self.versions[anchor]:

            self.versions[anchor].append(
                version
            )


        self.history.append({

            "event":
                "version.registered",

            "anchor":
                anchor,

            "version":
                version,

            "timestamp":
                time.time()

        })



    def current_version(self, anchor):

        versions = self.versions.get(
            anchor,
            []
        )

        if not versions:

            return None

        return sorted(
            versions
        )[-1]



    def register_migration(
        self,
        anchor,
        source,
        target,
        handler
    ):

        self.migrations.setdefault(
            anchor,
            []
        )


        self.migrations[anchor].append({

            "source":
                source,

            "target":
                target,

            "handler":
                handler

        })



    def can_upgrade(
        self,
        anchor,
        target
    ):

        current = self.current_version(
            anchor
        )


        if current is None:

            return {

                "valid":False,

                "reason":
                    "Unknown anchor"

            }



        for migration in self.migrations.get(
            anchor,
            []
        ):

            if (
                migration["source"] == current
                and
                migration["target"] == target
            ):

                return {

                    "valid":True,

                    "from":
                        current,

                    "to":
                        target

                }



        return {

            "valid":False,

            "reason":
                "Migration path unavailable"

        }



    def migrate(
        self,
        anchor,
        target
    ):

        check = self.can_upgrade(
            anchor,
            target
        )


        if not check["valid"]:

            return check



        for migration in self.migrations[anchor]:

            if (
                migration["source"]
                ==
                check["from"]

                and

                migration["target"]
                ==
                target
            ):

                result = migration["handler"]()


                self.register_version(
                    anchor,
                    target
                )


                return {

                    "success":True,

                    "result":
                        result,

                    "version":
                        target

                }


    def snapshot(self):

        return {

            "versions":
                self.versions,

            "migrations":
                {
                    key:
                    [
                        {
                            "source":m["source"],
                            "target":m["target"]
                        }

                        for m in value
                    ]

                    for key,value
                    in self.migrations.items()
                },

            "history":
                self.history

        }
PY




python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/anchors/__init__.py"
)


text = path.read_text()


if "AnchorVersionManager" not in text:

    text += """

from .versioning import AnchorVersionManager

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
    AnchorDependencyGraph,
)
""",

"""
    AnchorDependencyGraph,
    AnchorVersionManager,
)
"""

)



needle="""
self.anchor_dependencies = (
    AnchorDependencyGraph(
        self.anchor_registry
    )
)
"""


replacement="""

self.anchor_dependencies = (
    AnchorDependencyGraph(
        self.anchor_registry
    )
)


self.anchor_versions = (
    AnchorVersionManager(
        self.anchor_registry
    )
)

"""


text=text.replace(
needle,
replacement
)



if "anchor_version_status" not in text:

    text += """

    def anchor_version_status(self):

        return (
            self.anchor_versions
            .snapshot()
        )

"""



path.write_text(text)

PY





python -m compileall aletheus/runtime



python - <<'PY'

from aletheus.runtime import runtime_core


runtime_core.anchor_versions.register_version(
    "memory",
    "1.0"
)


runtime_core.anchor_versions.register_migration(
    "memory",
    "1.0",
    "2.0",
    lambda:
        {
            "migration":
            "memory schema upgraded"
        }
)



print({

"versions":
runtime_core.anchor_version_status(),

"upgrade":
runtime_core.anchor_versions.can_upgrade(
    "memory",
    "2.0"
),

"migration":
runtime_core.anchor_versions.migrate(
    "memory",
    "2.0"
),

"commands":
runtime_core.commands.count(),

"genesis":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY



echo "=== Genesis 8.7 Complete ==="

