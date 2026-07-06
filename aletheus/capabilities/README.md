# Capability Runtime Contract Update 01

Genesis 7.1 introduces the Capability Runtime Contract.

## Files

- `aletheus/capabilities/contract.py`
- `aletheus/capabilities/host.py`
- `aletheus/capabilities/__init__.py`

## Principle

Kernel governs.
Runtime hosts.
Capability delivers functionality.
Engine is an implementation detail.

## Verification

```bash
python -m py_compile \
  aletheus/capabilities/__init__.py \
  aletheus/capabilities/contract.py \
  aletheus/capabilities/host.py
```
