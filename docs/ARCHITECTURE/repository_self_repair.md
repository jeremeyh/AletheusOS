# Repository Self-Repair and Convergence Engine

The Repository Self-Repair subsystem continuously protects AletheusOS from repository drift, duplicate work trees, cache debris, accidental files, and unsafe merges.

## Constitutional behavior

- **Truth:** SHA-256 inventory determines identity; timestamps never decide correctness.
- **Integrity:** Every copied file is re-hashed after transfer.
- **Humility:** Divergent files are never auto-overwritten. The target is preserved and the source candidate is staged for review.
- **Continuity:** Source trees may be removed only after creation of a checksummed archive.
- **Reversibility:** Known debris is quarantined by default under `.aletheus_restore_points/`.

## Commands

Dry-run diagnosis and merge plan:

```bash
python tools/repository_self_repair/cli.py ~/Development/AletheusOS \
  --source "$HOME/Development/AletheusOS 2"
```

Apply safe merge and quarantine known debris:

```bash
python tools/repository_self_repair/cli.py ~/Development/AletheusOS \
  --source "$HOME/Development/AletheusOS 2" --apply
```

Apply, archive, verify, and remove the secondary tree:

```bash
python tools/repository_self_repair/cli.py ~/Development/AletheusOS \
  --source "$HOME/Development/AletheusOS 2" \
  --apply --archive-source --remove-source
```

Continuous hourly self-repair (non-merge mode):

```bash
python tools/repository_self_repair/cli.py ~/Development/AletheusOS \
  --monitor --interval 3600
```

## Safety boundaries

The engine does not auto-resolve different content at the same path. Conflicting source versions are staged beneath `.aletheus_restore_points/repository_conflicts/`. Permanent deletion requires `--delete-known-orphans`; source-tree removal requires both `--archive-source` and `--apply`.
