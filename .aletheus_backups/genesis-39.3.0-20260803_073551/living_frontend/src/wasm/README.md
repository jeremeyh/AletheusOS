# REM Rust/WASM boundary

`rem_kernel.rs` defines the first stable Rust/WASM computation boundary.

It is intentionally not compiled by the frontend build yet. It documents and
implements the deterministic Meantime Quotient kernel that will move into the
future `living_physics_core` crate.

Future integration:

```text
Telemetry Worker
  -> SharedArrayBuffer ring
  -> Rust/WASM RemKernel
  -> WebGPU storage buffer
  -> SIGHT projection
```
