from pathlib import Path

path = Path("aletheus/runtime/core.py")
text = path.read_text()

old = """            if service is not None:
                self.compat.register(
                    alias=alias,
                    implementation=service,
                )
"""

new = """            print(f"[COMPAT] {alias:12} -> {service is not None}")

            if service is not None:
                self.compat.register(
                    alias=alias,
                    implementation=service,
                )
"""

if old not in text:
    raise SystemExit("Registration block not found.")

text = text.replace(old, new, 1)

path.write_text(text)

print("✔ Compatibility debug logging enabled.")
