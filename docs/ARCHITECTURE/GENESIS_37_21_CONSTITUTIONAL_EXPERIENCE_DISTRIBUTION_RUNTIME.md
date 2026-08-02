# Genesis 37.21 — Constitutional Experience Production & Distribution Runtime™

Genesis 37.21 defines how the Constitutional Experience Intelligence stack is organized, built, validated, packaged, installed, upgraded, rolled back, and certified.

## Distribution Boundaries

- `core/physics` — Information Physics WASM output.
- `core/renderer` — AxiomUX WASM output and WGSL shaders.
- `core/navigation` — Hyperbolic navigation WASM output.
- `components/liquid_ui` — liquid materials and transition assemblies.
- `components/workspace_composer` — user-bounded dashboard composition.
- `applications/founder_observatory` — founder-root-only observability.
- `applications/mission_workspaces` — mission-centric living workspace runtime.
- `config` — templates, instruments, and physics rulesets.
- `manifests` — checksums, provenance, and build evidence.

## Installer Workflow

1. Validate repository and archive structure.
2. Create a timestamped backup.
3. Verify checksums.
4. Detect Python, Rust, WASM, WebGPU, and shader tooling.
5. Build or confirm required WASM outputs.
6. Validate WGSL sources where validators are available.
7. Hydrate workspace and instrument registries.
8. Assemble the distribution tree.
9. Run scoped tests and compilation checks.
10. Generate release evidence and stage a focused commit.

## Truthfulness Requirement

This package is source-first. It does not claim that production WASM binaries or host-driver WGSL validation have occurred when Cargo, wasm-pack, shader validators, or real source crates are unavailable.

## Founder Boundary

Founder Observatory remains founder-root-only. No admin permission, developer role, plugin hook, route registration, service discovery entry, or Workspace Composer instrument may grant access to it.
