from pathlib import Path

incoming = Path("uploads/incoming")

files = sorted(incoming.glob("*"))

print()
print("=" * 60)
print("UPLOAD QUEUE")
print("=" * 60)

if not files:
    print("No assets waiting.")
else:
    for f in files:
        print(f.name)

print("=" * 60)
