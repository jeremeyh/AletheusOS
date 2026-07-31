from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# -------------------------------------------------------
# Import
# -------------------------------------------------------

if "from aletheus.distributed_v3 import distributed_v3_core" not in text:
    text = text.replace(
        "from aletheus.planning_v2 import planning_core\n",
        "from aletheus.planning_v2 import planning_core\n"
        "from aletheus.distributed_v3 import distributed_v3_core\n",
    )

# -------------------------------------------------------
# Runtime initialization
# -------------------------------------------------------

if "self.distributed_v3 = distributed_v3_core" not in text:
    text = text.replace(
        "self.planning_v2 = planning_core",
        "self.planning_v2 = planning_core\n"
        "        self.distributed_v3 = distributed_v3_core",
        1,
    )

# -------------------------------------------------------
# Version
# -------------------------------------------------------

text = text.replace('self.version = "2.9.0"', 'self.version = "3.0.0"')

# -------------------------------------------------------
# Service Registration
# -------------------------------------------------------

if "Aletheus Distributed Runtime Fabric" not in text:
    marker = 'self.services.register("Aletheus Autonomous Planning Engine"'

    start = text.find(marker)

    if start != -1:
        end = text.find("\n", start)

        insertion = """

        self.services.register(
            "Aletheus Distributed Runtime Fabric",
            {
                "status": "online",
                "version": self.distributed_v3.VERSION,
            },
        )

"""

        text = text[: end + 1] + insertion + text[end + 1 :]

# -------------------------------------------------------
# Command Registration
# -------------------------------------------------------

if 'self.commands.register("cluster.bootstrap"' not in text:
    anchor = 'self.commands.register("plan.statistics", self._cmd_plan_statistics)'

    if anchor not in text:
        raise SystemExit("Could not locate planning command block.")

    text = text.replace(
        anchor,
        anchor
        + """

        # =====================================================
        # v3.0 Distributed Runtime Fabric
        # =====================================================

        self.commands.register("cluster.bootstrap", self._cmd_cluster_bootstrap)
        self.commands.register("cluster.join", self._cmd_cluster_join)
        self.commands.register("cluster.leave", self._cmd_cluster_leave)
        self.commands.register("cluster.nodes", self._cmd_cluster_nodes)
        self.commands.register("cluster.services", self._cmd_cluster_services)
        self.commands.register("cluster.heartbeat", self._cmd_cluster_heartbeat)
        self.commands.register("cluster.elect_leader", self._cmd_cluster_elect_leader)
        self.commands.register("cluster.status", self._cmd_cluster_status)
        self.commands.register("cluster.statistics", self._cmd_cluster_statistics)

""",
        1,
    )

core.write_text(text)

print("✔ v3.0 Runtime integration complete.")
