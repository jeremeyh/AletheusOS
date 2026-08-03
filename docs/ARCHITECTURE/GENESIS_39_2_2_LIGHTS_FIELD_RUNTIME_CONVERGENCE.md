# Genesis 39.2.2 — LIGHTS™ Field Runtime Convergence

## Canonical purpose

Genesis 39.2.2 converts the stabilized telemetry and metrology surface into a shared field runtime foundation.

The interface is not a screen. It is a responsive field.

## Additions

- `LIGHTSProvider` as the bounded owner of field state
- canonical phase derivation
- shared resonance and respiration
- typed density and founder-mode mutation
- deterministic metrology integration
- field-body physical variables
- ambient 8–12 second respiration
- automatic installer rollback on failed checks
- payload lexical validation to prevent malformed source bytes

## Boundaries

```text
Constitutional Runtime
        |
Information Physics
        |
LIGHTSProvider
        |
+-------+---------+
|                 |
SIGHT observer    Metrology
|                 |
AxiomUX bodies    Instruments
```

React remains the composition layer. Physical state and calculations remain in runtime and provider boundaries.

## Release safety

This package corrects the failures discovered in Genesis 39.2.1:

- no leading backslash in `lights-engine.ts`
- React `useRef` receives an explicit initial value
- valid metrology option names (`fftBins`, `channelCount`, `smoothing`, `seed`)
- `MetrologySnapshot` imported from `types.ts`
- explicit FFT callback types
- dependency verification for `framer-motion`
- transactional rollback if type checking, build, or focused tests fail
