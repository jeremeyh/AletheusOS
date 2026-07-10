#!/bin/bash

echo "======================================"
echo " AletheusOS System Integrity Test"
echo "======================================"


python - <<'PY'


print("")
print("AletheusOS Boot Test")
print("--------------------")


from aletheus.runtime.core import AletheusRuntime


runtime = AletheusRuntime()


print(
    runtime.health()
)



print("")
print("Module Import Test")
print("------------------")


modules = [

"aletheus.agents",
"aletheus.prediction",
"aletheus.knowledge_graph",
"aletheus.runtime",
"aletheus.business",
"aletheus.platform",
"aletheus.marketplace",
"card_hawk"

]


for module in modules:

    try:

        __import__(module)

        print(
            "[PASS]",
            module
        )

    except Exception as e:

        print(
            "[FAIL]",
            module,
            e
        )



print("")
print("AletheusOS Test Complete")



PY

