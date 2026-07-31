import importlib
import pkgutil

from core.engine_adapter import EngineAdapter
from core.engine_registry import engine_registry


class Discovery:
    def discover_package(self, package_name):

        package = importlib.import_module(package_name)

        discovered = []
        registered = []

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            full_name = f"{package_name}.{module_name}"

            try:
                module = importlib.import_module(full_name)

                discovered.append(full_name)

                if hasattr(module, "ENGINE"):
                    engine = module.ENGINE

                else:
                    engine = EngineAdapter(module)

                engine_registry.register(engine.name, engine)

                registered.append(engine.name)

            except Exception as exc:
                print("Discovery skipped:", full_name, exc)

        return discovered, registered


discovery = Discovery()
