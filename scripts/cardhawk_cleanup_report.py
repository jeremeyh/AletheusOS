from pathlib import Path

root = Path(".")
print("CardHawk OS™ Cleanup Report")
print("- services/ exists:", (root / "services").exists())
print("- services(space)/ exists:", (root / "services ").exists())
print("- platform/ exists:", (root / "platform").exists())
print("- cardhawk_platform/ exists:", (root / "cardhawk_platform").exists())
print()
print("Recommended manual cleanup after app launches cleanly:")
print("1. Rename 'services ' to '_deprecated_services_space'")
print("2. Rename 'platform' to '_deprecated_platform'")
print("3. Keep 'services' and 'cardhawk_platform' as canonical")
