from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# -------------------------------------------------------------------
# Ensure compatibility registry is imported
# -------------------------------------------------------------------

imp = "from aletheus.runtime.compat import compatibility_registry"

if imp not in text:
    anchor = "from aletheus.runtime.kernel import"

    idx = text.find(anchor)

    if idx == -1:
        raise SystemExit("Kernel import block not found.")

    end = text.find("\n", idx)

    text = text[: end + 1] + imp + "\n" + text[end + 1 :]

# -------------------------------------------------------------------
# Replace initialization with lazy bootstrap
# -------------------------------------------------------------------

old = """
        self.compat = compatibility_registry

        self._register_compatibility_services()
        self._apply_compatibility_aliases()
"""

new = """
        self.compat = compatibility_registry
"""

text = text.replace(old, new)

# -------------------------------------------------------------------
# Add lazy bootstrap helper
# -------------------------------------------------------------------

if "def _bootstrap_compatibility(self):" not in text:
    helper = """

    # ==========================================================
    # Runtime Compatibility Bootstrap
    # ==========================================================

    def _bootstrap_compatibility(self):

        if getattr(self, "_compat_initialized", False):
            return

        self._compat_initialized = True

        self._register_compatibility_services()

        self._apply_compatibility_aliases()

"""

    anchor = "    def _register_compatibility_services"

    if anchor not in text:
        raise SystemExit("_register_compatibility_services() not found.")

    text = text.replace(anchor, helper + anchor, 1)

# -------------------------------------------------------------------
# Every compat command bootstraps automatically
# -------------------------------------------------------------------

commands = [
    "_cmd_compat_list",
    "_cmd_compat_resolve",
    "_cmd_compat_statistics",
    "_cmd_compat_contract",
]

for cmd in commands:
    target = f"def {cmd}(self, context: RuntimeContext)"

    if target in text:
        text = text.replace(
            target,
            target + "\n\n        self._bootstrap_compatibility()",
            1,
        )

# -------------------------------------------------------------------
# Kernel bootstrap should initialize compat once
# -------------------------------------------------------------------

kernel = "def _cmd_kernel_bootstrap(self, context: RuntimeContext)"

if kernel in text:
    text = text.replace(
        kernel,
        kernel + "\n\n        self._bootstrap_compatibility()",
        1,
    )

core.write_text(text)

print("✔ Runtime Compatibility Layer bootstrap fixed.")
