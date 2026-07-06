# Executive Context Update 01

Complete Executive Kernel package with Executive Context.

Includes:
- context.py
- kernel.py
- registry.py
- capabilities.py
- policies.py
- decisions.py
- bus.py
- __init__.py

Principle:
Executive Kernel coordinates. Executive Context owns executive composition.
Runtime core remains protected.

Verification:
python -m py_compile \
  aletheus/executive_kernel/__init__.py \
  aletheus/executive_kernel/kernel.py \
  aletheus/executive_kernel/context.py \
  aletheus/executive_kernel/registry.py \
  aletheus/executive_kernel/capabilities.py \
  aletheus/executive_kernel/policies.py \
  aletheus/executive_kernel/decisions.py \
  aletheus/executive_kernel/bus.py
