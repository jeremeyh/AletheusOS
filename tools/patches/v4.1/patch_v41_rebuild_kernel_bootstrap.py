from pathlib import Path
import re

core = Path("aletheus/runtime/core.py")
text = core.read_text()

pattern = re.compile(
    r"def _cmd_kernel_bootstrap\(self,\s*context:\s*RuntimeContext.*?def _cmd_kernel_execute",
    re.S,
)

replacement = '''def _cmd_kernel_bootstrap(self, context: RuntimeContext) -> RuntimeContext:

        self._bootstrap_compatibility()

        context.add_result(
            "kernel",
            {
                "version": self.intelligence_orchestrator.version,
                "scheduler": self.intelligence_scheduler.statistics(),
                "dispatcher": self.intelligence_dispatcher.statistics(),
                "supervisor": self.intelligence_supervisor.statistics(),
                "health": "healthy",
            },
        )

        return context


    def _cmd_kernel_execute'''

text, count = pattern.subn(replacement, text, count=1)

if count != 1:
    raise SystemExit(
        "Could not uniquely locate _cmd_kernel_bootstrap().\n"
        "Run:\n"
        "nl -ba aletheus/runtime/core.py | sed -n '3310,3375p'"
    )

core.write_text(text)

print("✔ Rebuilt _cmd_kernel_bootstrap().")
