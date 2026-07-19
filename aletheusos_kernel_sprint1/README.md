# AletheusOS Constitutional Kernel

Sprint 1 proves the first executable constitutional vertical slice:

Constitution → Kernel → Runtime → Lifecycle → Registry → Event Bus → Mission → Evidence → Learning

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python main.py
pytest
```
