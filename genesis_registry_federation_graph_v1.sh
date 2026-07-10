#!/bin/bash

set -e

echo "================================================"
echo " AletheusOS Registry Federation Graph v1"
echo " Genesis 12.2"
echo "================================================"


DIR="aletheus/registry_federation"


cat > "$DIR/graph.py" <<'PY'
"""
AletheusOS Registry Federation Graph

Genesis 12.2

Builds an intelligence graph representing:
registries, engines, capabilities,
and runtime relationships.
"""


from pathlib import Path
import json


class RegistryFederationGraph:


    def __init__(
        self,
        base_path="aletheus/registry_federation"
    ):

        self.base_path = Path(base_path)

        self.nodes = {}
        self.edges = []


    def load_json(self, filename):

        path = self.base_path / filename

        if not path.exists():

            return {}

        return json.loads(
            path.read_text()
        )


    def add_node(
        self,
        node_id,
        node_type,
        metadata=None
    ):

        self.nodes[node_id] = {

            "type": node_type,

            "metadata":
                metadata or {}

        }


    def add_edge(
        self,
        source,
        target,
        relation
    ):

        self.edges.append({

            "source":
                source,

            "target":
                target,

            "relation":
                relation

        })


    def build(self):

        registry_map = self.load_json(
            "registry_map.json"
        )


        report = self.load_json(
            "wiring_report.json"
        )


        for registry in registry_map:

            self.add_node(
                registry,
                "registry"
            )


        for item in report:

            if isinstance(item, dict):

                name = (
                    item.get("name")
                    or
                    item.get("engine")
                    or
                    item.get("component")
                )

                if name:

                    self.add_node(
                        name,
                        "component",
                        item
                    )

                    self.add_edge(
                        name,
                        "runtime",
                        "attached"
                    )


        return self.snapshot()



    def snapshot(self):

        return {

            "nodes":
                self.nodes,

            "edges":
                self.edges,

            "node_count":
                len(self.nodes),

            "edge_count":
                len(self.edges)

        }



if __name__ == "__main__":

    graph = RegistryFederationGraph()

    print(
        json.dumps(
            graph.build(),
            indent=2
        )
    )

PY


python3 -m compileall "$DIR/graph.py"


echo ""
echo "Registry Federation Graph Created"
echo "================================================"

