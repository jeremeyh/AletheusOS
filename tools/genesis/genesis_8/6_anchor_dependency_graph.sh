#!/bin/bash

set -e

echo "=== Genesis 8.6 Anchor Dependency Graph ==="


mkdir -p aletheus/runtime/anchors



cat > aletheus/runtime/anchors/dependency.py <<'PY'
"""
Anchor Dependency Graph

Genesis 8.6

Provides dependency awareness for Runtime Anchor Circuits.
"""


class AnchorDependencyGraph:


    def __init__(self, registry):

        self.registry = registry

        self.dependencies = {}



    def register_dependency(
        self,
        anchor,
        requires
    ):

        self.dependencies.setdefault(
            anchor,
            []
        )

        if requires not in self.dependencies[anchor]:

            self.dependencies[anchor].append(
                requires
            )



    def dependencies_for(self, anchor):

        return self.dependencies.get(
            anchor,
            []
        )



    def validate(self):

        violations = []

        for anchor, deps in self.dependencies.items():

            for dependency in deps:

                if dependency not in self.registry.list():

                    violations.append({

                        "anchor":
                            anchor,

                        "missing_dependency":
                            dependency

                    })


        return {

            "valid":
                len(violations) == 0,

            "violations":
                violations

        }



    def startup_order(self):

        ordered = []

        visited = set()


        def visit(node):

            if node in visited:

                return

            visited.add(node)


            for dep in self.dependencies.get(
                node,
                []
            ):

                visit(dep)


            ordered.append(node)


        for anchor in self.registry.list():

            visit(anchor)


        return ordered



    def can_detach(self, anchor):

        blockers = []


        for name, deps in self.dependencies.items():

            if anchor in deps:

                blockers.append(name)


        return {

            "safe":
                len(blockers) == 0,

            "dependent_anchors":
                blockers

        }



    def snapshot(self):

        return {

            "dependencies":
                self.dependencies,

            "validation":
                self.validate(),

            "startup_order":
                self.startup_order()

        }
PY




python - <<'PY'

from pathlib import Path


path = Path(
"aletheus/runtime/anchors/__init__.py"
)


text = path.read_text()


if "AnchorDependencyGraph" not in text:

    text += """

from .dependency import AnchorDependencyGraph

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
    AnchorLifecycleController,
)
""",

"""
    AnchorLifecycleController,
    AnchorDependencyGraph,
)
"""

)



needle="""
self.anchor_lifecycle = (
    AnchorLifecycleController(
        self.anchor_registry
    )
)
"""


replacement="""

self.anchor_lifecycle = (
    AnchorLifecycleController(
        self.anchor_registry
    )
)


self.anchor_dependencies = (
    AnchorDependencyGraph(
        self.anchor_registry
    )
)

"""


text=text.replace(
needle,
replacement
)



if "anchor_dependency_status" not in text:

    text += """

    def anchor_dependency_status(self):

        return (
            self.anchor_dependencies
            .snapshot()
        )

"""



path.write_text(text)

PY





python -m compileall aletheus/runtime



python - <<'PY'

from aletheus.runtime import runtime_core


runtime_core.anchor_dependencies.register_dependency(
    "knowledge",
    "memory"
)

runtime_core.anchor_dependencies.register_dependency(
    "application",
    "knowledge"
)

runtime_core.anchor_dependencies.register_dependency(
    "intelligence",
    "memory"
)


print({

"dependencies":
runtime_core.anchor_dependency_status(),

"lifecycle":
runtime_core.anchor_lifecycle_status(),

"governance":
runtime_core.anchor_governance_status(),

"commands":
runtime_core.commands.count(),

"genesis":
runtime_core.genesis6_validate()["passed"],

"freeze":
runtime_core.genesis6_freeze_review()["approved"]

})

PY



echo "=== Genesis 8.6 Complete ==="

