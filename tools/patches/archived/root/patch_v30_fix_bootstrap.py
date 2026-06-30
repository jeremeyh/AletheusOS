from pathlib import Path
import re

path = Path("aletheus/distributed_v3/distributed_core.py")
text = path.read_text()

pattern = re.compile(
    r"def bootstrap\(self\):.*?def join",
    re.S,
)

replacement = '''
def bootstrap(self):
        """
        Initialize the local distributed cluster and always
        return cluster statistics expected by the runtime tests.
        """

        if self.cluster is None:

            self.cluster = RuntimeCluster(
                name="AletheusOS Primary Cluster"
            )

            founder = RuntimeNode(
                node_name="Founder Runtime",
                capabilities=[
                    "kernel",
                    "memory",
                    "knowledge",
                    "reasoning",
                    "decision",
                    "agents",
                    "workflow",
                    "planning",
                ],
                services=[
                    "Runtime Core",
                    "Memory Mesh",
                    "Knowledge Graph",
                    "Reasoning Engine",
                    "Decision Engine",
                    "Agent Runtime",
                    "Workflow Engine",
                    "Planning Engine",
                ],
            )

            self.cluster.nodes[founder.node_id] = founder
            self.cluster.leader_node_id = founder.node_id

        return self.statistics()

    def join'''

text2, count = pattern.subn(replacement, text)

if count != 1:
    raise SystemExit("Could not patch bootstrap().")

path.write_text(text2)

print("✔ Distributed bootstrap patched.")
