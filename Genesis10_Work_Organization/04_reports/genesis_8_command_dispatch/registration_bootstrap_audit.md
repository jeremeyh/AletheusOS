# Genesis 8 Registration Bootstrap Audit

## Summary

- registration_modules: **37**
- fully_live_modules: **31**
- partially_or_fully_missing_modules: **6**
- unreferenced_missing_modules: **0**
- modules_with_import_errors: **0**

## `aletheus.runtime.registrations.application_commands`

- File: `aletheus/runtime/registrations/application_commands.py`
- Functions: `register_application_commands`
- Loadable functions: `register_application_commands`
- Missing commands: `application.bootstrap.defaults`, `application.events`, `application.health`, `application.install`, `application.list`, `application.manifest`, `application.register`, `application.restart`, `application.start`, `application.stats`, `application.stop`, `application.uninstall`
- Referenced by bootstrap: `True`
- References for `register_application_commands`:
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:29:from aletheus.runtime.registrations.application_commands import register_application_commands`
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:48:register_application_commands,`

## `aletheus.runtime.registrations.executive_commands`

- File: `aletheus/runtime/registrations/executive_commands.py`
- Functions: `register_executive_commands`
- Loadable functions: `register_executive_commands`
- Missing commands: `executive.daily_brief`, `executive.recommendations`, `executive.risks`, `executive.snapshot`, `executive.status`, `executive.summary`, `executive.system_report`
- Referenced by bootstrap: `True`
- References for `register_executive_commands`:
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:33:from aletheus.runtime.registrations.executive_commands import register_executive_commands`
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:50:register_executive_commands,`

## `aletheus.runtime.registrations.planning_commands`

- File: `aletheus/runtime/registrations/planning_commands.py`
- Functions: `register_planning_commands`
- Loadable functions: `register_planning_commands`
- Missing commands: `plan.generate`, `plan.list`
- Referenced by bootstrap: `True`
- References for `register_planning_commands`:
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:36:from aletheus.runtime.registrations.planning_commands import register_planning_commands`
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:52:register_planning_commands,`

## `aletheus.runtime.registrations.semantic_commands`

- File: `aletheus/runtime/registrations/semantic_commands.py`
- Functions: `register_semantic_commands`
- Loadable functions: `register_semantic_commands`
- Missing commands: `semantic.assert`, `semantic.bootstrap.cardhawk`, `semantic.concept.create`, `semantic.concept.search`, `semantic.explain`, `semantic.query`, `semantic.stats`
- Referenced by bootstrap: `True`
- References for `register_semantic_commands`:
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:37:from aletheus.runtime.registrations.semantic_commands import register_semantic_commands`
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:49:register_semantic_commands,`

## `aletheus.runtime.registrations.uil_commands`

- File: `aletheus/runtime/registrations/uil_commands.py`
- Functions: `register_uil_commands`
- Loadable functions: `register_uil_commands`
- Missing commands: `uil.brief`, `uil.context`, `uil.decide`, `uil.reason`, `uil.snapshot`, `uil.stats`, `uil.synthesize`, `uil.timeline`
- Referenced by bootstrap: `True`
- References for `register_uil_commands`:
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:38:from aletheus.runtime.registrations.uil_commands import register_uil_commands`
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:54:register_uil_commands,`

## `aletheus.runtime.registrations.workspace_commands`

- File: `aletheus/runtime/registrations/workspace_commands.py`
- Functions: `register_workspace_commands`
- Loadable functions: `register_workspace_commands`
- Missing commands: `founder.journal.create`, `founder.journal.list`, `notification.create`, `notification.list`, `objective.create`, `objective.list`, `workspace.overview`, `workspace.stats`
- Referenced by bootstrap: `True`
- References for `register_workspace_commands`:
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:39:from aletheus.runtime.registrations.workspace_commands import register_workspace_commands`
  - `aletheus/runtime/command_bootstrap/bootstrapper.py:47:register_workspace_commands,`