# Genesis 8 Command Contract Probe

- Registered commands: 170
- Generation: 170
- Fingerprint: `7015c02ca06ed392279f59d46a724540cdad461d0093a358cba771c3597db647`

## `plugin.bootstrap`

- Registered: **True**
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.bootstrap`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/plugin.py:5`
- Signature: `(payload=None)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def bootstrap(self, payload=None):
        return self.runtime.plugins_v3.bootstrap()
```

## `plugin.install`

- Registered: **True**
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.install`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/plugin.py:8`
- Signature: `(payload)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def install(self, payload):
        return self.runtime.plugins_v3.install(**payload)
```

## `plugin.statistics`

- Registered: **True**
- Handler: `aletheus.runtime.domains.plugin.PluginDomain.statistics`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/plugin.py:38`
- Signature: `(payload=None)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def statistics(self, payload=None):
        return self.runtime.plugins_v3.statistics()
```

## `kernel.bootstrap`

- Registered: **True**
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.bootstrap`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/kernel.py:5`
- Signature: `(payload=None)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def bootstrap(self, payload=None):
        return {
            "version": self.runtime.intelligence_orchestrator.version,
            "scheduler": self.runtime.intelligence_scheduler.statistics(),
            "dispatcher": self.runtime.intelligence_dispatcher.statistics(),
            "supervisor": self.runtime.intelligence_supervisor.statistics(),
            "health": "healthy",
        }
```

## `kernel.execute`

- Registered: **True**
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.execute`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/kernel.py:14`
- Signature: `(payload)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def execute(self, payload):
        return self.runtime.intelligence_orchestrator.execute(
            command=payload.get("command"),
            payload=payload.get("payload", {}),
            runtime=self.runtime,
            priority=payload.get("priority", 5),
        )
```

## `kernel.tasks`

- Registered: **True**
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.tasks`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/kernel.py:22`
- Signature: `(payload=None)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def tasks(self, payload=None):
        return self.runtime.intelligence_orchestrator.list_tasks()
```

## `kernel.scheduler`

- Registered: **True**
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.scheduler`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/kernel.py:25`
- Signature: `(payload)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def scheduler(self, payload):
        if payload.get("task_id"):
            return self.runtime.intelligence_scheduler.schedule(
                payload["task_id"],
                payload.get("priority", 5),
            )

        return self.runtime.intelligence_scheduler.statistics()
```

## `kernel.dispatcher`

- Registered: **True**
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.dispatcher`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/kernel.py:34`
- Signature: `(payload)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def dispatcher(self, payload):
        if payload.get("command"):
            dispatched = self.runtime.intelligence_dispatcher.dispatch(
                runtime=self.runtime,
                command=payload["command"],
                payload=payload.get("payload", {}),
            )

            return {
                "results": dispatched.results,
                "errors": dispatched.errors,
            }

        return self.runtime.intelligence_dispatcher.statistics()
```

## `kernel.supervisor`

- Registered: **True**
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.supervisor`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/kernel.py:49`
- Signature: `(payload=None)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def supervisor(self, payload=None):
        return self.runtime.intelligence_supervisor.check(self.runtime)
```

## `kernel.statistics`

- Registered: **True**
- Handler: `aletheus.runtime.domains.kernel.KernelDomain.statistics`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/domains/kernel.py:52`
- Signature: `(payload=None)`
- Invocation mode: `payload`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def statistics(self, payload=None):
        return {
            "orchestrator": self.runtime.intelligence_orchestrator.statistics(),
            "scheduler": self.runtime.intelligence_scheduler.statistics(),
            "dispatcher": self.runtime.intelligence_dispatcher.statistics(),
            "supervisor": self.runtime.intelligence_supervisor.statistics(),
        }
```

## `runtime.doctor`

- Registered: **True**
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.doctor`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/adapters/runtime_adapter.py:76`
- Signature: `(context)`
- Invocation mode: `context`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def doctor(self, context):

        context.add_result(
            "doctor",
            self.runtime.diagnostics(),
        )

        return context
```

## `runtime.invariants`

- Registered: **True**
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.invariants`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/adapters/runtime_adapter.py:86`
- Signature: `(context)`
- Invocation mode: `context`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def invariants(self, context):

        context.add_result(
            "invariants",
            self.runtime.invariants(),
        )

        return context
```

## `runtime.boot.validate`

- Registered: **True**
- Handler: `aletheus.runtime.adapters.runtime_adapter.RuntimeCommandAdapter.boot_validate`
- Location: `/Users/master_lord_6ixth/Development/AletheusOS/aletheus/runtime/adapters/runtime_adapter.py:96`
- Signature: `(context)`
- Invocation mode: `context`
- Category: `general`
- Description: ``
- Metadata: `{}`

```python
    def boot_validate(self, context):

        context.add_result(
            "boot_validation",
            self.runtime.boot_certification_validate(),
        )

        return context
```

## `runtime.health_report`

- Registered: **False**
