# Nimble™ Interaction Grammar

## Purpose

Nimble™ interaction must feel direct, fluid, responsive, spatial,
and understandable.

The user should feel that they are manipulating the platform itself,
not submitting requests into an opaque interface.

## Core Rules

### Directness

Actions should occur as close as possible to the object they affect.

### Continuity

Objects should preserve visual and spatial identity while moving,
resizing, docking, expanding, or changing state.

### Interruptibility

Long-running transitions and operations must remain interruptible
whenever interruption is technically safe.

### Reversibility

Reversible actions must expose undo or restoration.

Irreversible actions must disclose impact before execution.

### Visibility

Every interaction must communicate:

- current state,
- accepted input,
- operation progress,
- completion,
- failure,
- and available recovery.

### Consistency

Equivalent actions must behave consistently across AletheusOS and all
inheriting applications.

## Input Modes

Nimble™ must support:

- pointer,
- keyboard,
- touch,
- gesture,
- command palette,
- natural-language command,
- and assistive technology.

No primary capability may depend exclusively on hover, drag, color,
or animation.

## Direct Manipulation

Supported direct-manipulation behaviors may include:

- drag,
- resize,
- reorder,
- dock,
- undock,
- group,
- select,
- multi-select,
- connect,
- inspect,
- expand,
- collapse,
- zoom,
- and pan.

Every direct-manipulation action must have a keyboard-accessible
equivalent where practical.

## Latency Feedback

Under 100 milliseconds:
- no explicit loading treatment is required.

Between 100 and 500 milliseconds:
- provide subtle acknowledgement.

Between 500 milliseconds and 2 seconds:
- show visible progress or active state.

Beyond 2 seconds:
- expose progress, status, cancellation when safe, and background
  continuation where supported.

Motion must never conceal latency.

## Principle X

The interaction layer must never hide:

- system uncertainty,
- validation failure,
- partial completion,
- permission denial,
- destructive impact,
- or recovery options.
