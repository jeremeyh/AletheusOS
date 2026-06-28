from pathlib import Path
import ast

class DependencyGraph:
    """Builds a lightweight dependency map of Python imports."""

    @staticmethod
    def build(root="."):
        root = Path(root)
        graph = {}

        for path in root.rglob("*.py"):
            if any(part in {".venv", "venv", "__pycache__"} for part in path.parts):
                continue

            try:
                tree = ast.parse(path.read_text(errors="ignore"))
            except Exception:
                continue

            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.extend(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imports.append(node.module)

            graph[str(path)] = sorted(set(imports))

        return graph

    @staticmethod
    def internal_only(graph):
        prefixes = (
            "assets", "asset_core", "components", "services", "engines", "engine",
            "workflow", "marketplace", "portfolio", "intelligence", "scout",
            "hawk_aeye", "cardhawk_aeye", "thorx", "pipeline", "eventbus",
            "datalake", "founder", "providers", "marketplace_normalizer",
            "continuous_scout", "negotiation", "genome", "config", "registry"
        )
        return {
            file: [imp for imp in imports if imp.startswith(prefixes)]
            for file, imports in graph.items()
        }
