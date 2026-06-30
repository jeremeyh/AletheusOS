from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

old = '''            print(f"[COMPAT] {alias:12} -> {service is not None}")

            if service is not None:
                self.compat.register(
                    alias=alias,
                    implementation=service,
                )
'''

new = '''            if service is not None:
                self.compat.register(
                    alias=alias,
                    implementation=service,
                )
'''

if old not in text:
    raise SystemExit(
        "Compatibility debug logging was not found (it may already be removed)."
    )

text = text.replace(old, new, 1)

core.write_text(text)

print("✔ Removed temporary compatibility debug logging.")
