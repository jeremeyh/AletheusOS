from aletheus.runtime.builder import RuntimeBuilder

runtime = (
    RuntimeBuilder()
    .development()
    .plugins(True)
    .enterprise(False)
    .clustered(False)
    .build()
)

print("========================================================")
print("ALETHEUSOS RUNTIME BUILDER")
print("========================================================")
print()

for key, value in runtime.items():
    if key == "container":
        print(f"{key:<15}: RuntimeContainer")
    else:
        print(f"{key:<15}: {value}")

print()
print("========================================================")
