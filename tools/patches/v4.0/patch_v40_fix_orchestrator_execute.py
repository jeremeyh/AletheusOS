from pathlib import Path

path = Path("aletheus/runtime/kernel/orchestrator.py")
text = path.read_text()

old = """            context = runtime.commands.dispatch(
                task.command,
                task.payload,
            )

            task.result = context.results
            task.errors = context.errors
            task.status = "failed" if context.errors else "completed"
"""

new = """            # Dispatch directly through the runtime command bus.
            # Avoid routing back through the kernel executor.
            context = runtime.commands.dispatch(
                task.command,
                task.payload,
            )

            task.result = dict(context.results)
            task.errors = list(context.errors)

            if context.errors:
                task.status = "failed"
            else:
                task.status = "completed"
"""

if old not in text:
    raise SystemExit("execute_task() block not found. Patch manually.")

text = text.replace(old, new, 1)

path.write_text(text)

print("✔ Patched IntelligenceOrchestrator.execute_task().")
