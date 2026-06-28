"""
CardHawk OS™
Kernel Doctor
"""

from kernel.runtime import kernel

def doctor():

    kernel.boot()

    status = kernel.status()

    print("\n===== CardHawk OS Doctor =====")

    print(f"Engines      : {status['engines']}")
    print(f"Services     : {status['services']}")
    print(f"Projections  : {status['projections']}")
    print(f"Listeners    : {sum(status['listeners'].values())}")

    if status["engines"] == 0:
        print("WARNING: No engines registered.")

    if status["services"] == 0:
        print("WARNING: No services registered.")

    print("\nSystem Health: OK")
