from pathlib import Path

path = Path("aletheus/planning_v2/planning_core.py")
text = path.read_text()

if "def register_default_plans" not in text:
    insert = """

    # ----------------------------------------------------
    # Runtime Compatibility API
    # ----------------------------------------------------

    def register_default_plans(self):
        return self.bootstrap()

    def version(self):
        return self.VERSION

    def list_plans(self):
        return [
            plan.to_dict()
            for plan in self.plans.values()
        ]

"""

    anchor = "    def statistics(self):"

    if anchor not in text:
        raise SystemExit("statistics() not found.")

    text = text.replace(anchor, insert + "\n" + anchor, 1)

path.write_text(text)

print("✔ Planning runtime compatibility added.")
