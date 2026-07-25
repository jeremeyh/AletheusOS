import os
import sys

print("\n========== PYTEST IMPORT DEBUG ==========")
print("Executable:", sys.executable)
print("CWD:", os.getcwd())
print("sys.path:")
for i, p in enumerate(sys.path):
    print(f"{i:2}: {p}")

try:
    import nimble
    print("nimble:", nimble.__file__)
except Exception as e:
    print("nimble import failed:", repr(e))

print("=========================================\n")
