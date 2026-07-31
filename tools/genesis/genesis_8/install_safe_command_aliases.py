# ... all of your existing script above this point ...


call_line = "        register_compatibility_alias_commands(runtime)"

if call_line not in bootstrap_text:
    anchor = "        register_governance_commands(runtime)"

    if anchor not in bootstrap_text:
        raise RuntimeError("Governance registration anchor not found.")

    bootstrap_text = bootstrap_text.replace(
        anchor,
        (
            anchor
            + "\n\n"
            + "        # Explicit compile-time compatibility aliases.\n"
            + call_line
        ),
        1,
    )


BOOTSTRAPPER.write_text(
    bootstrap_text,
    encoding="utf-8",
)

alias_count = len(ALIAS_MODULE.read_text(encoding="utf-8").splitlines())

print("Genesis 8 safe command aliases installed.")
print(f"Backup: {backup.relative_to(ROOT)}")
print(f"Created: {ALIAS_MODULE.relative_to(ROOT)}")
print(f"Updated: {BOOTSTRAPPER.relative_to(ROOT)}")
print(f"Alias count: {alias_count}")
