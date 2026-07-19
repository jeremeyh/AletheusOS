# Nimble Production Gate Evidence

Generated: `2026-07-10T23:00:16.004274+00:00`

## Result

- Status: **PASS**
- Exit code: `0`
- Duration: `7.36s`
- Commit: `eb53711`
- Branch: `feature/cardhawk-streamlit-v0.1`
- Working tree dirty: `True`

## Runtime

- Python: `3.14.6`
- Node: `v24.18.0`
- npm: `11.16.0`
- Platform: `macOS-26.5.1-arm64-arm-64bit-Mach-O`

## Bundle

- Primary: `index-CW82vOQv.js`
- Primary bytes: `447,168`
- Primary budget: `500,000`
- Within budget: **True**
- Secondary chunks: `6`

### JavaScript chunks

| Chunk | Kind | Bytes |
|---|---:|---:|
| `CommandHistoryRoute-DyL4T3mF.js` | secondary | 3,144 |
| `CommandSurface-DoMPExIX.js` | secondary | 49,389 |
| `OidcCallbackRoute-Be4BGyS7.js` | secondary | 1,228 |
| `commandQueries-Bjv7rfLL.js` | secondary | 3,455 |
| `index-CW82vOQv.js` | primary | 447,168 |
| `oidc-client-ts-C_veRLI2.js` | secondary | 67,533 |
| `oidcSession-BQVirP6V.js` | secondary | 12,967 |

## Gate output

```text

> @aletheus/nimble-workspace@0.1.0 typecheck
> npm run typecheck --workspaces --if-present


> @aletheus/nimble-shell@0.1.0 typecheck
> tsc -b --pretty false


> @aletheus/nimble-core@0.1.0 typecheck
> tsc -p tsconfig.json --noEmit --pretty false


> @aletheus/nimble-motion@0.1.0 typecheck
> tsc -p tsconfig.json --noEmit --pretty false


> @aletheus/nimble-react@0.1.0 typecheck
> tsc -p tsconfig.json --noEmit --pretty false


> @aletheus/nimble-testing@0.1.0 typecheck
> tsc -p tsconfig.json --noEmit --pretty false


> @aletheus/nimble-transparency@0.1.0 typecheck
> tsc -p tsconfig.json --noEmit --pretty false


> @aletheus/nimble-workspace-engine@0.1.0 typecheck
> tsc -p tsconfig.json --noEmit --pretty false


> @aletheus/nimble-workspace@0.1.0 test
> npm run test --workspaces --if-present --run

npm warn Unknown cli config "--run". This will stop working in the next major version of npm.

> @aletheus/nimble-shell@0.1.0 test
> vitest run --config vitest.config.ts


[1m[30m[46m RUN [49m[39m[22m [36mv4.1.10 [39m[90m/Users/master_lord_6ixth/Development/AletheusOS/nimble/apps/platform-shell[39m

 [32m✓[39m src/nimble/api/__tests__/lazyImport.test.ts [2m([22m[2m3 tests[22m[2m)[22m[32m 6[2mms[22m[39m
 [32m✓[39m src/nimble/api/__tests__/commandTypes.test.ts [2m([22m[2m1 test[22m[2m)[22m[32m 2[2mms[22m[39m
 [32m✓[39m src/nimble/api/__tests__/commandHistory.test.ts [2m([22m[2m2 tests[22m[2m)[22m[32m 2[2mms[22m[39m
 [32m✓[39m src/nimble/api/__tests__/commandEligibility.test.ts [2m([22m[2m3 tests[22m[2m)[22m[32m 5[2mms[22m[39m
 [32m✓[39m src/nimble/api/__tests__/oidcSession.test.ts [2m([22m[2m2 tests[22m[2m)[22m[32m 23[2mms[22m[39m
 [32m✓[39m src/nimble/api/__tests__/apiTransport.test.ts [2m([22m[2m3 tests[22m[2m)[22m[32m 5[2mms[22m[39m
 [32m✓[39m src/nimble/api/__tests__/prefetch.test.ts [2m([22m[2m4 tests[22m[2m)[22m[32m 255[2mms[22m[39m

[2m Test Files [22m [1m[32m7 passed[39m[22m[90m (7)[39m
[2m      Tests [22m [1m[32m18 passed[39m[22m[90m (18)[39m
[2m   Start at [22m 18:00:20
[2m   Duration [22m 1.25s[2m (transform 198ms, setup 0ms, import 232ms, tests 296ms, environment 5.82s)[22m


> @aletheus/nimble-workspace@0.1.0 build
> npm run build --workspace @aletheus/nimble-shell


> @aletheus/nimble-shell@0.1.0 build
> tsc -b && vite build

[36mvite v8.1.4 [32mbuilding client environment for production...[36m[39m
[2K
transforming...✓ 621 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                                0.54 kB │ gzip:   0.32 kB
dist/assets/index-BYV9smdh.css                38.02 kB │ gzip:   6.92 kB
dist/assets/OidcCallbackRoute-Be4BGyS7.js      1.22 kB │ gzip:   0.59 kB
dist/assets/CommandHistoryRoute-DyL4T3mF.js    3.14 kB │ gzip:   1.13 kB
dist/assets/commandQueries-Bjv7rfLL.js         3.45 kB │ gzip:   1.28 kB
dist/assets/oidcSession-BQVirP6V.js           12.96 kB │ gzip:   4.76 kB
dist/assets/CommandSurface-DoMPExIX.js        49.38 kB │ gzip:  16.10 kB
dist/assets/oidc-client-ts-C_veRLI2.js        67.53 kB │ gzip:  17.04 kB
dist/assets/index-CW82vOQv.js                447.16 kB │ gzip: 141.84 kB

[32m✓ built in 126ms[39m
========================================================================
NIMBLE™ FOUNDATION VALIDATION
========================================================================
Manifest: valid
Engine contracts: valid
Application inheritance: valid
Token schema: valid
Required engines: 10
Status: PASS
========================================================================
NIMBLE™ TOKEN VALIDATION
========================================================================
Primitive groups: 7
Semantic themes: 2
Motion groups: 6
Generated outputs: 3
Status: PASS
========================================================================
NIMBLE™ COMPONENT FOUNDATION VALIDATION
========================================================================
Component categories: 9
Component contracts: 6
Interaction contracts: 7
Workspace capabilities: 7
Accessibility standard: present
Principle X enforcement: active
Status: PASS
========================================================================
NIMBLE™ REFERENCE SHELL VALIDATION
========================================================================
Rendered shell: present
Implemented engines: 8
Implemented surfaces: 9
Advanced motion: present
Command interaction: present
State persistence: present
Reduced motion: present
Principle X disclosure: active
Status: PASS
PASS: Nimble bundle boundary is valid.
Primary: nimble/apps/platform-shell/dist/assets/index-CW82vOQv.js (447168 bytes)
OIDC lazy chunk: nimble/apps/platform-shell/dist/assets/oidc-client-ts-C_veRLI2.js (67533 bytes)
OIDC lazy chunk: nimble/apps/platform-shell/dist/assets/oidcSession-BQVirP6V.js (12967 bytes)
PASS: Nimble route splitting is valid.
Primary: nimble/apps/platform-shell/dist/assets/index-CW82vOQv.js (447168 bytes)
Secondary chunks: 6
- nimble/apps/platform-shell/dist/assets/CommandHistoryRoute-DyL4T3mF.js (3144 bytes)
- nimble/apps/platform-shell/dist/assets/CommandSurface-DoMPExIX.js (49389 bytes)
- nimble/apps/platform-shell/dist/assets/OidcCallbackRoute-Be4BGyS7.js (1228 bytes)
- nimble/apps/platform-shell/dist/assets/commandQueries-Bjv7rfLL.js (3455 bytes)
- nimble/apps/platform-shell/dist/assets/oidc-client-ts-C_veRLI2.js (67533 bytes)
- nimble/apps/platform-shell/dist/assets/oidcSession-BQVirP6V.js (12967 bytes)
========================================================================
NIMBLE™ CI VALIDATION
========================================================================
Workflow: present
Python runtime: configured
Node 24 runtime: configured
Deterministic npm install: configured
Gateway tests: configured
Production gate: configured
Build artifacts: retained
Concurrency control: active
Status: PASS

========================================================================
FRONTEND TYPECHECK
========================================================================
Command: /Users/master_lord_6ixth/.nvm/versions/node/v24.18.0/bin/npm run typecheck
Directory: nimble
PASS: Frontend typecheck (2.64s)

========================================================================
FRONTEND TESTS
========================================================================
Command: /Users/master_lord_6ixth/.nvm/versions/node/v24.18.0/bin/npm run test -- --run
Directory: nimble
PASS: Frontend tests (1.81s)

========================================================================
FRONTEND PRODUCTION BUILD
========================================================================
Command: /Users/master_lord_6ixth/.nvm/versions/node/v24.18.0/bin/npm run build
Directory: nimble
PASS: Frontend production build (1.62s)

========================================================================
NIMBLE FOUNDATION
========================================================================
Command: /Users/master_lord_6ixth/Development/AletheusOS/.venv/bin/python validate_nimble_foundation.py
Directory: .
PASS: Nimble foundation (0.06s)

========================================================================
NIMBLE TOKENS
========================================================================
Command: /Users/master_lord_6ixth/Development/AletheusOS/.venv/bin/python validate_nimble_tokens.py
Directory: .
PASS: Nimble tokens (0.05s)

========================================================================
NIMBLE COMPONENTS
========================================================================
Command: /Users/master_lord_6ixth/Development/AletheusOS/.venv/bin/python validate_nimble_components.py
Directory: .
PASS: Nimble components (0.05s)

========================================================================
NIMBLE REFERENCE SHELL
========================================================================
Command: /Users/master_lord_6ixth/Development/AletheusOS/.venv/bin/python validate_nimble_reference_shell.py
Directory: .
PASS: Nimble reference shell (0.04s)

========================================================================
NIMBLE BUNDLE BOUNDARY
========================================================================
Command: /Users/master_lord_6ixth/Development/AletheusOS/.venv/bin/python validate_nimble_bundle_boundary.py
Directory: .
PASS: Nimble bundle boundary (0.04s)

========================================================================
NIMBLE ROUTE SPLITTING
========================================================================
Command: /Users/master_lord_6ixth/Development/AletheusOS/.venv/bin/python validate_nimble_route_splitting.py
Directory: .
PASS: Nimble route splitting (0.04s)

========================================================================
NIMBLE CI CONTRACT
========================================================================
Command: /Users/master_lord_6ixth/Development/AletheusOS/.venv/bin/python validate_nimble_ci.py
Directory: .
PASS: Nimble CI contract (0.04s)

========================================================================
NIMBLE BUNDLE BUDGET
========================================================================
Primary: nimble/apps/platform-shell/dist/assets/index-CW82vOQv.js
Size: 447,168 bytes
Limit: 500,000 bytes
Secondary chunks: 6
Status: PASS

========================================================================
NIMBLE™ PRODUCTION GATE
========================================================================
Checks completed: 11
Frontend type safety: PASS
Frontend tests: PASS
Production build: PASS
Architecture contracts: PASS
Reference implementation: PASS
OIDC bundle isolation: PASS
Route splitting: PASS
Primary bundle budget: PASS
Elapsed: 6.38s
Status: PASS
```
