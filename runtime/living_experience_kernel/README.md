# Living Experience Kernel

This crate is the Genesis 39.3 Rust/WASM boundary for off-thread temporal
determinism and morphogenesis processing.

Build when `wasm-pack` is available:

```bash
wasm-pack build --target web --release
```

The installer does not falsely report a WASM build when `wasm-pack` is absent.
It records the build as deferred and preserves the source boundary.
