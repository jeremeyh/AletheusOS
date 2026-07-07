import ast
from pathlib import Path

from .models import CoreAnalysis


class RuntimeCoreAnalyzer:
    """
    Analyzes runtime/core.py without modifying it.
    """

    def __init__(self, path: str = "aletheus/runtime/core.py"):
        self.path = Path(path)

    def analyze(self) -> CoreAnalysis:
        text = self.path.read_text(errors="ignore")
        lines = text.splitlines()

        tree = ast.parse(text)

        functions = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        classes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

        imports = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]

        largest_functions = []

        for fn in functions:
            if hasattr(fn, "lineno") and hasattr(fn, "end_lineno"):
                size = fn.end_lineno - fn.lineno + 1
                largest_functions.append(
                    {
                        "name": fn.name,
                        "line": fn.lineno,
                        "size": size,
                    }
                )

        largest_functions.sort(
            key=lambda item: item["size"],
            reverse=True,
        )

        return CoreAnalysis(
            path=str(self.path),
            line_count=len(lines),
            function_count=len(functions),
            class_count=len(classes),
            import_count=len(imports),
            largest_functions=largest_functions[:15],
        )
