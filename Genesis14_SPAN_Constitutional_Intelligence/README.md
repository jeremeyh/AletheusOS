# AletheusOS Genesis 14.0 Release Package

## Where this folder goes

Place the extracted folder directly inside the **AletheusOS project root**.

Correct:

```text
AletheusOS/
├── aletheus/
├── reports/
├── Genesis14_SPAN_Constitutional_Intelligence/
│   ├── install.sh
│   ├── validate.sh
│   ├── rollback.sh
│   └── package/
└── ...
```

Do **not** place it inside `aletheus/`, `aletheus/span/`, `tools/`, or `reports/`.

## Install

From the AletheusOS project root:

```bash
chmod +x Genesis14_SPAN_Constitutional_Intelligence/*.sh
./Genesis14_SPAN_Constitutional_Intelligence/install.sh
```

The installer copies the release payload to:

```text
AletheusOS/aletheus/span/
```

It creates:

```text
aletheus/span/api.py
aletheus/span/constitutional_context.py
aletheus/span/profiles.py
aletheus/span/reporter.py
aletheus/span/rules/*.py
aletheus/span/profiles/*.yaml
aletheus/span/docs/GENESIS14.md
tests/span/test_genesis14.py
```

It also adds guarded Genesis 14 public exports to:

```text
aletheus/span/__init__.py
```

## Validate

```bash
./Genesis14_SPAN_Constitutional_Intelligence/validate.sh
```

## Roll back

The installer writes a timestamped backup under:

```text
reports/span/backups/genesis14_<UTC timestamp>/
```

To restore the latest backup:

```bash
./Genesis14_SPAN_Constitutional_Intelligence/rollback.sh
```
