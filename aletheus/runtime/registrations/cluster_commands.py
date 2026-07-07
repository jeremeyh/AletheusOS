"""
Cluster Command Registration

Genesis 6
"""

def register_cluster_commands(runtime):

    commands = runtime.commands

    commands.register("cluster.create", runtime._cmd_cluster_create)
    commands.register("cluster.bootstrap", runtime._cmd_cluster_bootstrap)
    commands.register("cluster.join", runtime._cmd_cluster_join)
    commands.register("cluster.leave", runtime._cmd_cluster_leave)
    commands.register("cluster.nodes", runtime._cmd_cluster_nodes)
    commands.register("cluster.services", runtime._cmd_cluster_services)
    commands.register("cluster.heartbeat", runtime._cmd_cluster_heartbeat)
    commands.register("cluster.elect_leader", runtime._cmd_cluster_elect_leader)
    commands.register("cluster.statistics", runtime._cmd_cluster_statistics)
    commands.register("cluster.list", runtime._cmd_cluster_list)
    commands.register("cluster.status", runtime._cmd_cluster_status)
    commands.register("cluster.broadcast", runtime._cmd_cluster_broadcast)
    commands.register("cluster.task.assign", runtime._cmd_cluster_task_assign)
    commands.register("cluster.history", runtime._cmd_cluster_history)
    commands.register("cluster.stats", runtime._cmd_cluster_stats)
    commands.register("node.register", runtime._cmd_node_register)
    commands.register("node.remove", runtime._cmd_node_remove)
    commands.register("node.heartbeat", runtime._cmd_node_heartbeat)
