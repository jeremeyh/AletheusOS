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
