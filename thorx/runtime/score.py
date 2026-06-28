FACTORS = [
    "Scarcity",
    "Player",
    "Demand",
    "Liquidity",
    "Visual Appeal",
    "Population",
    "Upside"
]

print()
print("THORX SCORE")
print("=" * 40)

score = 0

for i,f in enumerate(FACTORS,1):
    print(i,f)
    score += 10

print()
print("Demo Score:",score)
