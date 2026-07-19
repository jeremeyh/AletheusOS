from aletheus.planning_v2 import planning_core

print("VERSION:", planning_core.VERSION)

print("bootstrap:", hasattr(planning_core, "bootstrap"))
print("register_default_plans:", hasattr(planning_core, "register_default_plans"))
print("create:", hasattr(planning_core, "create"))
print("execute:", hasattr(planning_core, "execute"))
print("progress:", hasattr(planning_core, "progress"))
print("replan:", hasattr(planning_core, "replan"))
print("complete:", hasattr(planning_core, "complete"))
print("statistics:", hasattr(planning_core, "statistics"))
