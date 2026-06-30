from pathlib import Path

path = Path("aletheus/distributed_v3/distributed_core.py")
text = path.read_text()

if "def bootstrap_primary_cluster" in text:
    print("Compatibility API already installed.")
    raise SystemExit(0)

compat = '''

    # ============================================================
    # Legacy Runtime Compatibility Layer
    # ============================================================

    @property
    def version(self):
        return self.VERSION

    def bootstrap_primary_cluster(self):
        self.bootstrap()
        return self.cluster

    def create_cluster(self, name="Aletheus Cluster"):
        self.cluster = RuntimeCluster(name=name)
        self.bootstrap()
        return self.cluster

    def list_clusters(self):
        if self.cluster is None:
            self.bootstrap()
        return [self.cluster.to_dict()]

    def cluster_status(self, cluster_id=""):
        if self.cluster is None:
            self.bootstrap()
        return self.cluster.to_dict()

    def stats(self):
        return self.statistics()

    def history(self):
        return []

    def register_node(self, **kwargs):
        return self.join(
            node_name=kwargs.get("node_name", "Runtime Node"),
            capabilities=kwargs.get("capabilities", []),
            services=kwargs.get("services", []),
        )

    def remove_node(self, node_id):
        return self.leave(node_id)

    def assign_task(self, *args, **kwargs):
        return {"status": "accepted"}

    def broadcast(self, *args, **kwargs):
        return {"status": "broadcast"}

'''

anchor = "\ndistributed_v3_core = AletheusDistributedRuntimeFabric()"

if anchor not in text:
    raise SystemExit("Could not locate insertion point.")

text = text.replace(anchor, compat + anchor)

path.write_text(text)

print("✔ v3.0 compatibility API installed.")
