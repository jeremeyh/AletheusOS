from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

old = """    def _cmd_cluster_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        cluster = self.distributed.bootstrap_primary_cluster()
        self.kernel_v2.publish(
            event_type="cluster.bootstrapped",
            source="distributed_fabric",
            payload=cluster.to_dict(),
        )
        context.add_result("cluster", cluster.to_dict())
        return context
"""

new = """    def _cmd_cluster_bootstrap(self, context: RuntimeContext) -> RuntimeContext:
        cluster = self.distributed.bootstrap_primary_cluster()

        self.kernel_v2.publish(
            event_type="cluster.bootstrapped",
            source="distributed_fabric",
            payload=cluster.to_dict(),
        )

        # Return runtime statistics expected by the v3.0 tests
        context.add_result(
            "cluster",
            self.distributed.stats(),
        )

        return context
"""

if old not in text:
    raise SystemExit("Could not locate _cmd_cluster_bootstrap().")

text = text.replace(old, new, 1)

path.write_text(text)

print("✔ Patched _cmd_cluster_bootstrap() to return cluster statistics.")
