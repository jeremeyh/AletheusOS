# Guardian Kernel™ Report

Generated: 2026-07-01T09:23:06.314421
Version: 1.0.0

## Decision

- Allowed: False
- Mode: block_and_scan
- Message: Critical event blocked. Watch Tower scan requested.

## Guardian Payload

```json
{
  "version": "1.0.0",
  "timestamp": "2026-07-01T09:23:06.314421",
  "event": {
    "source": "core-stack-test",
    "action": "delete",
    "target": "vault",
    "risk": "critical",
    "allowed": false,
    "conclave_status": "blocked_protected_destructive",
    "watch_tower_requested": true,
    "principle_x_required": true,
    "created_at": "2026-07-01T09:23:04.471551"
  },
  "conclave": {
    "version": "1.0.0",
    "timestamp": "2026-07-01T09:23:04.469470",
    "source": "core-stack-test",
    "action": "delete",
    "target": "vault",
    "classification": "blocked_protected_destructive",
    "risk": "critical",
    "allowed": false,
    "response": "block, shield, decoy, audit, request Watch Tower scan, activate Principle X",
    "principle_x": true,
    "watch_tower_requested": true,
    "shield_engaged": true,
    "decoy": {
      "status": "shielded",
      "data": {},
      "message": "No sensitive data available."
    }
  },
  "watch_tower": {
    "version": "1.0.0",
    "root": "/Users/master_lord_6ixth/Development/AletheusOS",
    "generated_at": "2026-07-01T09:23:06.312731",
    "status": "watching",
    "score": 0,
    "counts": {
      "critical": 0,
      "high": 0,
      "medium": 70,
      "low": 61
    },
    "repairs": [],
    "findings": [
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: .DS_Store",
        "path": ".DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.833898"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: founder/.DS_Store",
        "path": "founder/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.834954"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: database/.DS_Store",
        "path": "database/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.835164"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: pipeline/.DS_Store",
        "path": "pipeline/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.835250"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: migrations/.DS_Store",
        "path": "migrations/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.835371"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: eventbus/.DS_Store",
        "path": "eventbus/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.835566"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: tools/.DS_Store",
        "path": "tools/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.835653"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: asset_core/.DS_Store",
        "path": "asset_core/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.835771"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: core/.DS_Store",
        "path": "core/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.836021"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: production_hardening/.DS_Store",
        "path": "production_hardening/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.836193"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: intelligence/.DS_Store",
        "path": "intelligence/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.836432"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: config/.DS_Store",
        "path": "config/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.836532"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: security/.DS_Store",
        "path": "security/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.836632"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: cardhawkos/.DS_Store",
        "path": "cardhawkos/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.836836"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: contracts/.DS_Store",
        "path": "contracts/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.837220"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: marketplace/.DS_Store",
        "path": "marketplace/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.837604"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: runtime/.DS_Store",
        "path": "runtime/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.837874"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: workflows/.DS_Store",
        "path": "workflows/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.838325"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: qa/.DS_Store",
        "path": "qa/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.838562"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: datalake/.DS_Store",
        "path": "datalake/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.838735"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: release/.DS_Store",
        "path": "release/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.838812"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: adaptive_intelligence/.DS_Store",
        "path": "adaptive_intelligence/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.839050"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: live_data/.DS_Store",
        "path": "live_data/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.839390"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: hawk_aeye/.DS_Store",
        "path": "hawk_aeye/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.839683"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: integrations/.DS_Store",
        "path": "integrations/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.839902"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: live_platform/.DS_Store",
        "path": "live_platform/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.840078"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: components/.DS_Store",
        "path": "components/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.840155"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: aletheus/.DS_Store",
        "path": "aletheus/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.840507"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: founder_studio/.DS_Store",
        "path": "founder_studio/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.840834"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: founder_ai/.DS_Store",
        "path": "founder_ai/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.841034"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: deal_finder/.DS_Store",
        "path": "deal_finder/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.841121"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: engines/.DS_Store",
        "path": "engines/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.841291"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: ai/.DS_Store",
        "path": "ai/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.841412"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: data_providers/.DS_Store",
        "path": "data_providers/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.841624"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: executive_experience/.DS_Store",
        "path": "executive_experience/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.841862"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: data_layer/.DS_Store",
        "path": "data_layer/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.842059"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: diagnostics/.DS_Store",
        "path": "diagnostics/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.842150"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: applications/.DS_Store",
        "path": "applications/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.842233"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: portfolio/.DS_Store",
        "path": "portfolio/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.842374"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: operations_live/.DS_Store",
        "path": "operations_live/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.842585"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: command_center/.DS_Store",
        "path": "command_center/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.842661"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: negotiation/.DS_Store",
        "path": "negotiation/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.843044"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: jobs/.DS_Store",
        "path": "jobs/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.843141"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: thorx/.DS_Store",
        "path": "thorx/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.843346"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: versioning/.DS_Store",
        "path": "versioning/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.843473"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: genome/.DS_Store",
        "path": "genome/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.843554"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: intelligence_convergence/.DS_Store",
        "path": "intelligence_convergence/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.843694"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: startup/.DS_Store",
        "path": "startup/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.843842"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: timeline/.DS_Store",
        "path": "timeline/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.844206"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: pages/.DS_Store",
        "path": "pages/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.844293"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: engine/.DS_Store",
        "path": "engine/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.844373"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: themes/.DS_Store",
        "path": "themes/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.844547"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: falcon/.DS_Store",
        "path": "falcon/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.844691"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: decision_engine/.DS_Store",
        "path": "decision_engine/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.844889"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: nest/.DS_Store",
        "path": "nest/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.844973"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: orchestrator/.DS_Store",
        "path": "orchestrator/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.845157"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: kernel/.DS_Store",
        "path": "kernel/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.845249"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: analytics/.DS_Store",
        "path": "analytics/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.845409"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: event_bus/.DS_Store",
        "path": "event_bus/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:04.845602"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: aletheus/runtime/.DS_Store",
        "path": "aletheus/runtime/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.047827"
      },
      {
        "code": "CACHE_ARTIFACT",
        "severity": "low",
        "title": "Disposable system artifact found",
        "message": "Safe cleanup candidate: aletheus/runtime/guardian/.DS_Store",
        "path": "aletheus/runtime/guardian/.DS_Store",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.054728"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: metrics",
        "path": "metrics",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.106135"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools",
        "path": "tools",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.106785"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: platform",
        "path": "platform",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.108143"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: marketplace",
        "path": "marketplace",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.108400"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: scheduler",
        "path": "scheduler",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.108848"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: observability",
        "path": "observability",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.109695"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: workflow",
        "path": "workflow",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.111229"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: scripts",
        "path": "scripts",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.111360"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: diagnostics",
        "path": "diagnostics",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.111504"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: cardhawk_platform",
        "path": "cardhawk_platform",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.111780"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: thorx",
        "path": "thorx",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.112455"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: pages",
        "path": "pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.113220"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: themes",
        "path": "themes",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.113578"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: backups",
        "path": "backups",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.113655"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: founder/runtime",
        "path": "founder/runtime",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.115465"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: database/migrations",
        "path": "database/migrations",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.115750"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: database/seed",
        "path": "database/seed",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.115829"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/verification",
        "path": "tools/verification",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.117172"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/cleanup",
        "path": "tools/cleanup",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.117245"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/maintenance",
        "path": "tools/maintenance",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.117321"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/migration",
        "path": "tools/migration",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.117459"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: production_hardening/pages",
        "path": "production_hardening/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.118516"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: workflow_automation/pages",
        "path": "workflow_automation/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.121058"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: marketplace/parsers",
        "path": "marketplace/parsers",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.121249"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: marketplace/pricing",
        "path": "marketplace/pricing",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.121454"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: runtime/registrations",
        "path": "runtime/registrations",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.123684"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/research",
        "path": "adaptive_intelligence/research",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125329"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/quality",
        "path": "adaptive_intelligence/quality",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125410"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/plugins",
        "path": "adaptive_intelligence/plugins",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125483"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/simulation",
        "path": "adaptive_intelligence/simulation",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125555"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/explainability",
        "path": "adaptive_intelligence/explainability",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125636"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/feedback",
        "path": "adaptive_intelligence/feedback",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125740"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/deployment",
        "path": "adaptive_intelligence/deployment",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125830"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/governance",
        "path": "adaptive_intelligence/governance",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125898"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: adaptive_intelligence/pages",
        "path": "adaptive_intelligence/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.125981"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: live_data/providers",
        "path": "live_data/providers",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.126477"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: live_data/comps",
        "path": "live_data/comps",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.126566"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: live_data/pages",
        "path": "live_data/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.126635"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: live_data/pricing",
        "path": "live_data/pricing",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.126704"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: live_data/watchlist",
        "path": "live_data/watchlist",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.126774"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: live_platform/pages",
        "path": "live_platform/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.128701"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: founder_studio/pages",
        "path": "founder_studio/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.132507"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: cardhawk/web",
        "path": "cardhawk/web",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.132999"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: executive_experience/pages",
        "path": "executive_experience/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.136874"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: data_layer/importers",
        "path": "data_layer/importers",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.137152"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: data_layer/exporters",
        "path": "data_layer/exporters",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.137223"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: data_layer/repositories",
        "path": "data_layer/repositories",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.137299"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: portfolio/health",
        "path": "portfolio/health",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.137846"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: operations_live/pages",
        "path": "operations_live/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.138255"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: thorx/runtime",
        "path": "thorx/runtime",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.139357"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: intelligence_convergence/engines",
        "path": "intelligence_convergence/engines",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.139923"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: intelligence_convergence/pages",
        "path": "intelligence_convergence/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.140020"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: timeline/demo",
        "path": "timeline/demo",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.140913"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: timeline/pages",
        "path": "timeline/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.141160"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: backups/runtime",
        "path": "backups/runtime",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.142364"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: analytics/runtime",
        "path": "analytics/runtime",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.144159"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: analytics/pages",
        "path": "analytics/pages",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.144256"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v4.2",
        "path": "tools/patches/v4.2",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.366974"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v4.3",
        "path": "tools/patches/v4.3",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367076"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v4.4",
        "path": "tools/patches/v4.4",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367195"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v5.0",
        "path": "tools/patches/v5.0",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367282"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v2",
        "path": "tools/patches/v2",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367369"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v3",
        "path": "tools/patches/v3",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367507"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v4.1",
        "path": "tools/patches/v4.1",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367585"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v4.6",
        "path": "tools/patches/v4.6",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367661"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v4.0",
        "path": "tools/patches/v4.0",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367743"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v3.7",
        "path": "tools/patches/v3.7",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367880"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/patches/v3.9",
        "path": "tools/patches/v3.9",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.367950"
      },
      {
        "code": "INIT_MISSING",
        "severity": "medium",
        "title": "Missing package initializer",
        "message": "Python package appears to need __init__.py: tools/experiments/debug",
        "path": "tools/experiments/debug",
        "repairable": true,
        "created_at": "2026-07-01T09:23:05.368083"
      },
      {
        "code": "ARCHITECTURE_DUPLICATE_MARKER",
        "severity": "medium",
        "title": "Potential duplicate architecture packages",
        "message": "Both eventbus and event_bus exist. Confirm canonical ownership before deleting either.",
        "path": "eventbus, event_bus",
        "repairable": false,
        "created_at": "2026-07-01T09:23:05.814265"
      }
    ]
  },
  "principle_x": {
    "required": true,
    "mode": "integrity_supremacy",
    "message": "Principle X requires preservation over convenience."
  },
  "decision": {
    "allowed": false,
    "mode": "block_and_scan",
    "message": "Critical event blocked. Watch Tower scan requested."
  }
}
```
