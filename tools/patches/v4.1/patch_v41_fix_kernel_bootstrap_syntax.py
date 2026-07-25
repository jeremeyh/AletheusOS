import re
from pathlib import Path

core = Path("aletheus/runtime/core.py")
text = core.read_text()

# ------------------------------------------------------------------
# Fix any kernel bootstrap definition missing its colon
# ------------------------------------------------------------------

text = re.sub(
    r'def _cmd_kernel_bootstrap\(self,\s*context:\s*RuntimeContext\)\s*\n',
    'def _cmd_kernel_bootstrap(self, context: RuntimeContext):\n',
    text,
)

# ------------------------------------------------------------------
# Ensure bootstrap call is inside the function body
# ------------------------------------------------------------------

pattern = (
    "def _cmd_kernel_bootstrap(self, context: RuntimeContext):\n"
    "\n"
    "        self._bootstrap_compatibility()"
)

if pattern not in text:

    text = text.replace(
        "def _cmd_kernel_bootstrap(self, context: RuntimeContext):\n",
        "def _cmd_kernel_bootstrap(self, context: RuntimeContext):\n"
        "\n"
        "        self._bootstrap_compatibility()\n",
        1,
    )

core.write_text(text)

print("✔ Fixed _cmd_kernel_bootstrap syntax.")
