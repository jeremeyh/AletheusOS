const domains=[['▦','Workspace Studio','Workspaces & Execution'],['⌘','Builder Studio','Platform Engineering'],['>_','Admin Terminal','System & Governance'],['⌬','Platform Services','Core Services & Integrations'],['⌁','Analytics Studio','Insights & Telemetry'],['◇','Opus','Knowledge Civilization'],['◉','Mammoth','Storage Civilization'],['♙','Organizations','Teams & Tenants'],['♙','Users','Identity & Access'],['⬡','Security','Policy & Compliance']];
const activities=[['▦','10:54:32','Workspace Studio hydrated','System'],['◇','10:54:11','Opus knowledge graph synchronized','Opus'],['⌁','10:53:47','CRK kernel heartbeat','Runtime'],['</>','10:53:19','Builder Studio project compiled','Builder'],['◉','10:52:58','Evidence review surface ready','A3ye']];
const prompts=['What workspaces are currently active?','Verify system health and integrity','Show recent evidence collected','What is the current Qₘ stability?','List available platform services'];
const metrics=[['Active Workspaces','7','● Online'],['Constitutional Integrity','VERIFIED','No Violations'],['Qₘ Stability','91.4','NOMINAL'],['Runtime Health','OPTIMAL','All Systems Nominal'],['Evidence Items','127','Total Collected']];
const app=document.querySelector('#app');
app.innerHTML=`<div class="shell">
<header class="topbar"><div class="brand"><span class="aletheus-mark-breathe"><img src="./assets/aletheus-gold-mark.jpeg"></span><div><b>ALETHEUSOS</b><span>GENESIS 114</span></div></div><div class="context"><b>Workspace Studio</b><span>End-user workspaces, tools, and workflow execution</span></div><button id="commandSearch" class="search command-search" type="button" aria-label="Open command search"><span class="search-icon">⌕</span><span class="search-copy">Search or type a command...</span><kbd>⌘K</kbd></button><div class="tools">♧ ☼ ?</div><button id="a03toggle" class="a03-mini a3ye-trigger" aria-label="Open A3ye constitutional perception" aria-expanded="true"><img src="./assets/a03-lens-master.jpeg"><span>A3ye™</span></button><div class="founder"><b>Founder</b><span>6DM</span><i></i></div></header>
<aside class="sidebar"><label>OPERATING DOMAINS</label><nav>${domains.map((d,i)=>`<button class="domain ${i===0?'active':''}"><i>${d[0]}</i><span><b>${d[1]}</b><small>${d[2]}</small></span></button>`).join('')}</nav><div class="sysstatus"><span>System Status</span><b>● OPERATIONAL</b></div></aside>
<main class="main"><label>OVERVIEW</label><section class="metrics">${metrics.map((m,i)=>`<article><small>${m[0]}</small><strong class="m${i}">${m[1]}</strong><span>${m[2]}</span></article>`).join('')}</section>
<section class="grid"><article class="panel activity"><h3>RECENT ACTIVITY</h3>${activities.map(a=>`<div class="row"><i>${a[0]}</i><time>${a[1]}</time><b>${a[2]}</b><span>${a[3]}</span></div>`).join('')}<a>View all activity →</a></article><article class="panel telemetry"><h3>SYSTEM TELEMETRY</h3><div class="telegrid">${['CPU|18%','Memory|42%','GPU|22%','Qₘ Stability|91.4','FPS|60','Threads|128'].map((t,i)=>{let [l,v]=t.split('|');return`<div><small>${l}</small><b>${v}</b><svg viewBox="0 0 100 30"><polyline points="0,27 12,24 25,25 38,18 50,20 62,12 75,14 88,7 100,8"/></svg></div>`}).join('')}</div><a>View full telemetry →</a></article>
<article class="panel work"><h3>RECENT WORKSPACES</h3><div class="tiles"><div>▦ <span>Sentinel Operations<small>Active now</small></span></div><div>⬡ <span>Evidence Review<small>Active 5h ago</small></span></div><div>▣ <span>Project Aletheus<small>Active 2h ago</small></span></div><div>◇ <span>Enterprise Command<small>Active 1d ago</small></span></div></div><a>Open all workspaces →</a></article><article class="panel work"><h3>PINNED WORKSPACES</h3><div class="tiles"><div>⌘ <span>Builder Studio</span></div><div>◇ <span>Opus Knowledge</span></div><div>>_ <span>Admin Terminal</span></div><div>⚙ <span>Platform Services</span></div></div><a>Manage pinned →</a></article></section></main>
<aside id="perception" class="perception"><div class="phead"><div class="a03-word"><span>A</span><span class="a3ye-lens-identity"><img src="./assets/a03-lens-master.jpeg" alt=""></span><span>3ye™</span></div><button id="close">×</button></div><p>Constitutional Perception Platform</p><div class="ask"><span>Ask a question or request analysis...</span><button>➤</button></div><div class="tabs"><b>Recent</b><span>Suggested</span><span>Workspaces</span></div><div class="prompts">${prompts.map((p,i)=>`<button><span>${p}</span><time>10:${54-i} AM</time></button>`).join('')}</div><label>CAPABILITIES</label><div class="caps">${['Ask','Verify','Examine','Analyze','Forecast'].map((c,i)=>`<button><i>${['◌','⬡','⌕','△','↗'][i]}</i><span>${c}</span></button>`).join('')}</div><footer><i></i>A3ye perception surface ready. No live observation asserted.</footer></aside>
<footer class="bottom"><div class="dock"><button><img src="./assets/aletheus-gold-mark.jpeg"></button><button>📁</button><button>◇</button><button class="selected"><img src="./assets/a03-lens-master.jpeg"></button><button>>_</button><button>⌁</button><button>⚙</button></div><div class="runtime"><b>● LOCAL EXPERIENCE</b><span>Experience<strong>READY</strong></span><span>Runtime<strong>UNBOUND</strong></span><span>Telemetry<strong>NOT BOUND</strong></span><span>Build<strong>LOCAL</strong></span><span>Genesis<strong>114</strong></span><time>Workspace Studio<small>Genesis 114</small></time></div></footer></div>`;
const panel=document.querySelector('#perception');
const a3yeToggle=document.querySelector('#a03toggle');

function setA3yeOpen(open){
  panel.classList.toggle('hidden',!open);
  a3yeToggle.classList.toggle('is-active',open);
  a3yeToggle.setAttribute('aria-expanded',String(open));
}

document.querySelector('#close').onclick=()=>setA3yeOpen(false);
a3yeToggle.onclick=()=>setA3yeOpen(panel.classList.contains('hidden'));

a3yeToggle.addEventListener('mouseenter',()=>a3yeToggle.classList.add('is-aware'));
a3yeToggle.addEventListener('mouseleave',()=>a3yeToggle.classList.remove('is-aware'));

setA3yeOpen(true);
setInterval(()=>{const q=(91.2+Math.random()*.4).toFixed(1);document.querySelector('.m2').textContent=q;document.querySelectorAll('.telegrid>div')[3].querySelector('b').textContent=q;},1300);


const commandSearch=document.querySelector('#commandSearch');

function pulseA3yeState(state,duration=0){
  a3yeToggle.dataset.a3yeState=state;
  if(duration>0){
    window.setTimeout(()=>{
      if(a3yeToggle.dataset.a3yeState===state){
        a3yeToggle.dataset.a3yeState=panel.classList.contains('hidden')?'idle':'ready';
      }
    },duration);
  }
}

a3yeToggle.addEventListener('pointerdown',()=>pulseA3yeState('processing',650));

a3yeToggle.addEventListener('click',()=>{
  pulseA3yeState('thinking',1100);
});

commandSearch.addEventListener('click',()=>{
  commandSearch.classList.add('is-engaged');
  window.setTimeout(()=>commandSearch.classList.remove('is-engaged'),700);
});

document.addEventListener('keydown',(event)=>{
  if((event.metaKey||event.ctrlKey)&&event.key.toLowerCase()==='k'){
    event.preventDefault();
    commandSearch.focus();
    commandSearch.classList.add('is-engaged');
    window.setTimeout(()=>commandSearch.classList.remove('is-engaged'),700);
  }
});

pulseA3yeState('ready');

/* ALETHEUSOS_MC84F4E_CANON_RUNTIME_V1
 * Additive constitutional identity for the current Mission Control implementation.
 * Existing interaction and visual geometry above this block remain authoritative.
 */
;(() => {
  const release = Object.freeze({
    release: "MC84F4E",
    canonicalSurface: "Mission Control",
    implementationStrategy: "CURRENT_ADDITIVE_WITH_MC84F4D_PROTECTED_SURFACE_ASSERTIONS",
    visualParent: "MC84F4D",
    visualAncestor: "Genesis84",
    canonHead: "cca067c25cfdddbbd48e165cdb561eaf0f36f701",
    authorityPath: "docs/ARCHITECTURE/authority",
    canonicalSurfaces: Object.freeze([
      "Mission Control",
      "Workspace Studio",
      "Builder Studio",
      "Admin Terminal",
      "Platform Services",
      "Analytics Studio",
      "Opus",
      "Mammoth",
      "Founder",
      "A3ye"
    ]),
    knowledgeArchitecture: Object.freeze({
      Opus: "constitutional knowledge, documents, evidence, Genesis corpus, and institutional memory",
      Mammoth: "storage, persistence, indexing, replication, archival, recovery, and lifecycle infrastructure"
    }),
    protectedMissionControlSurfaces: Object.freeze([
      "outer shell",
      "top bar",
      "left navigation",
      "navigation geometry",
      "A3ye visual/lens/command plane",
      "search",
      "bottom dock and dock states",
      "runtime strip",
      "Living Intelligence Field",
      "global material/background grammar"
    ])
  });

  Object.defineProperty(globalThis, "AletheusOS_MC84F4E", {
    value: release,
    enumerable: false,
    configurable: false,
    writable: false
  });
})();

/* ALETHEUSOS_MC84F4F_RUNTIME_V1
 * Forward runtime evolution on published MC84F4E.
 * This layer adds constitutional surface observability and lineage introspection
 * without replacing or restyling the protected Mission Control UI.
 */
;(() => {
  const parent = globalThis.AletheusOS_MC84F4E;

  const canonicalSurfaces = Object.freeze([
    "Mission Control",
    "Workspace Studio",
    "Builder Studio",
    "Admin Terminal",
    "Platform Services",
    "Analytics Studio",
    "Opus",
    "Mammoth",
    "Founder",
    "A3ye"
  ]);

  const protectedSurfaces = Object.freeze([
    "outer shell",
    "top bar",
    "left navigation",
    "navigation geometry",
    "A3ye visual/lens/command plane",
    "search",
    "bottom dock and dock states",
    "runtime strip",
    "Living Intelligence Field",
    "global material/background grammar"
  ]);

  const normalize = value => String(value ?? "")
    .replace(/\s+/g, " ")
    .trim()
    .toLowerCase();

  const surfaceHints = Object.freeze({
    "Mission Control": Object.freeze(["mission control", "mission-control"]),
    "Workspace Studio": Object.freeze(["workspace studio", "workspace"]),
    "Builder Studio": Object.freeze(["builder studio", "builder"]),
    "Admin Terminal": Object.freeze(["admin terminal", "admin"]),
    "Platform Services": Object.freeze(["platform services", "services"]),
    "Analytics Studio": Object.freeze(["analytics studio", "analytics"]),
    "Opus": Object.freeze(["opus"]),
    "Mammoth": Object.freeze(["mammoth"]),
    "A3ye": Object.freeze(["a3ye", "a3ye", "3ye"])
  });

  const collectSurfaceSnapshot = () => {
    if (typeof document === "undefined" || typeof document.querySelectorAll !== "function") {
      return Object.freeze({
        environment: "non-dom",
        detected: Object.freeze([]),
        canonicalCount: canonicalSurfaces.length,
        protectedCount: protectedSurfaces.length
      });
    }

    const nodes = Array.from(document.querySelectorAll(
      '[aria-label],[title],[data-surface],button,a,[role="button"],nav,input,[placeholder]'
    ));

    const corpus = nodes.map(node => normalize([
      node.textContent,
      node.getAttribute?.("aria-label"),
      node.getAttribute?.("title"),
      node.getAttribute?.("data-surface"),
      node.getAttribute?.("placeholder")
    ].filter(Boolean).join(" "))).filter(Boolean);

    const detected = canonicalSurfaces.filter(surface => {
      const hints = surfaceHints[surface] || [normalize(surface)];
      return hints.some(hint => corpus.some(text => text.includes(normalize(hint))));
    });

    return Object.freeze({
      environment: "dom",
      detected: Object.freeze(detected),
      canonicalCount: canonicalSurfaces.length,
      protectedCount: protectedSurfaces.length
    });
  };

  const release = Object.freeze({
    release: "MC84F4F",
    parentRelease: "MC84F4E",
    canonicalSurface: "Mission Control",
    implementationMode: "forward-runtime-surface-registry",
    visualParent: "MC84F4D",
    visualAncestor: "Genesis84",
    canonHead: "dad8d7c17e152703687826b008a9a6a8ba0c1e87",
    canonicalSurfaces,
    protectedSurfaces,
    parentRuntimePresent: Boolean(parent),
    snapshot: collectSurfaceSnapshot
  });

  Object.defineProperty(globalThis, "AletheusOS_MC84F4F", {
    value: release,
    enumerable: false,
    configurable: false,
    writable: false
  });

  if (typeof document !== "undefined") {
    if (document.documentElement?.dataset) {
      document.documentElement.dataset.aletheusosMcRelease = "MC84F4F";
      document.documentElement.dataset.aletheusosMcParent = "MC84F4E";
    }

    if (typeof document.dispatchEvent === "function" && typeof CustomEvent === "function") {
      document.dispatchEvent(new CustomEvent("aletheusos:mc84f4f-ready", {
        detail: release.snapshot()
      }));
    }
  }
})();

/* ALETHEUSOS_MC84F4G_INTERACTION_BRIDGE_V1
 * Constitutional intent/capability evaluation layer.
 * Fail closed. No network, storage, backend, navigation, or privileged side effects.
 */
;(() => {
  const parent = globalThis.AletheusOS_MC84F4F;
  const capabilities = Object.freeze({
    "Mission Control": Object.freeze(["inspect","focus"]),
    "Workspace Studio": Object.freeze(["inspect","open"]),
    "Builder Studio": Object.freeze(["inspect","open"]),
    "Admin Terminal": Object.freeze(["inspect"]),
    "Platform Services": Object.freeze(["inspect"]),
    "Analytics Studio": Object.freeze(["inspect","open"]),
    "Opus": Object.freeze(["inspect","open"]),
    "Mammoth": Object.freeze(["inspect"]),
    "Founder": Object.freeze(["inspect"]),
    "A3ye": Object.freeze(["inspect","focus"])
  });
  const normalizeIntent = intent => Object.freeze({
    id: String(intent?.id ?? ""),
    surface: String(intent?.surface ?? ""),
    capability: String(intent?.capability ?? ""),
    payload: intent?.payload ?? null
  });
  const evaluate = intent => {
    const normalized = normalizeIntent(intent);
    const allowedCapabilities = capabilities[normalized.surface] || [];
    const allowed = Boolean(
      normalized.surface &&
      normalized.capability &&
      allowedCapabilities.includes(normalized.capability)
    );
    return Object.freeze({
      ...normalized,
      allowed,
      decision: allowed ? "ALLOW" : "REFUSE",
      parentRelease: parent?.release ?? null
    });
  };
  const release = Object.freeze({
    release: "MC84F4G",
    parentRelease: "MC84F4F",
    architecture: "CONSTITUTIONAL_INTERACTION_CAPABILITY_BRIDGE",
    canonicalSurface: "Mission Control",
    visualParent: "MC84F4D",
    visualAncestor: "Genesis84",
    canonHead: "fc0cf518707ab0a4dd610723b382ac2e43bc7ae4",
    capabilities,
    evaluate
  });
  Object.defineProperty(globalThis, "AletheusOS_MC84F4G", {
    value: release, enumerable: false, configurable: false, writable: false
  });
})();

/* ALETHEUSOS_MC84F4H_RUNTIME_DOCK_COORDINATOR_V1
 * Pure runtime/dock state semantics over F4G interaction decisions.
 * No protected visual mutation is performed.
 */
;(() => {
  const parent = globalThis.AletheusOS_MC84F4G;
  const states = Object.freeze(["idle","focused","engaged","degraded"]);
  const normalizeHealth = health => Object.freeze({
    parentRuntimePresent: Boolean(health?.parentRuntimePresent ?? true),
    snapshotAvailable: Boolean(health?.snapshotAvailable ?? true),
    protectedSurfaceCount: Number(health?.protectedSurfaceCount ?? 0)
  });
  const deriveState = ({ decision, health } = {}) => {
    const h = normalizeHealth(health);
    if (!h.parentRuntimePresent || !h.snapshotAvailable) return "degraded";
    if (decision?.decision === "ALLOW" && decision?.capability === "open") return "engaged";
    if (decision?.decision === "ALLOW") return "focused";
    return "idle";
  };
  const transition = input => Object.freeze({
    state: deriveState(input),
    previousState: states.includes(input?.previousState) ? input.previousState : "idle",
    parentRelease: parent?.release ?? null
  });
  const release = Object.freeze({
    release: "MC84F4H",
    parentRelease: "MC84F4G",
    architecture: "RUNTIME_DOCK_STATE_COORDINATOR",
    canonicalSurface: "Mission Control",
    visualParent: "MC84F4D",
    visualAncestor: "Genesis84",
    states,
    deriveState,
    transition
  });
  Object.defineProperty(globalThis, "AletheusOS_MC84F4H", {
    value: release, enumerable: false, configurable: false, writable: false
  });
})();

/* ALETHEUSOS_MC84F4I_ACCESSIBILITY_RESPONSIVE_HARDENING_V1
 * Final interaction hardening contract: audit and classify, never silently mutate.
 */
;(() => {
  const parent = globalThis.AletheusOS_MC84F4H;
  const classifyViewport = width => {
    const value = Number(width);
    if (!Number.isFinite(value) || value <= 0) return "unknown";
    if (value < 720) return "compact";
    if (value < 1200) return "standard";
    return "expanded";
  };
  const isActivationKey = key => key === "Enter" || key === " ";
  const accessibleName = node => String(
    node?.getAttribute?.("aria-label") ||
    node?.getAttribute?.("title") ||
    node?.textContent ||
    ""
  ).replace(/\s+/g," ").trim();
  const auditAccessibility = root => {
    const target = root || (typeof document !== "undefined" ? document : null);
    if (!target || typeof target.querySelectorAll !== "function") {
      return Object.freeze({ environment:"non-dom", checked:0, violations:Object.freeze([]) });
    }
    const nodes = Array.from(target.querySelectorAll('button,a,[role="button"],input,select,textarea'));
    const violations=[];
    for (const node of nodes) {
      const tag=String(node.tagName || "").toLowerCase();
      const type=String(node.getAttribute?.("type") || "").toLowerCase();
      const exempt=tag==="input" && type==="hidden";
      if (!exempt && !accessibleName(node)) violations.push("missing-accessible-name");
    }
    return Object.freeze({
      environment:"dom",
      checked:nodes.length,
      violations:Object.freeze(violations)
    });
  };
  const release = Object.freeze({
    release:"MC84F4I",
    parentRelease:"MC84F4H",
    architecture:"ACCESSIBILITY_RESPONSIVE_INTERACTION_HARDENING",
    canonicalSurface:"Mission Control",
    visualParent:"MC84F4D",
    visualAncestor:"Genesis84",
    classifyViewport,
    isActivationKey,
    auditAccessibility
  });
  Object.defineProperty(globalThis,"AletheusOS_MC84F4I",{
    value:release, enumerable:false, configurable:false, writable:false
  });
})();

/* ALETHEUSOS_MC_PLATFORM_READ_MODEL_BRIDGE_V1 */
(() => {
  "use strict";

  const RELEASE = "MC-PLATFORM-INTEGRATION-READ-MODEL-V1";
  const PARENT_RELEASE = "MC84F4I";
  const F4G_METHOD = "evaluate";
  const PLATFORM_READ_MODEL = {"a3ye_general_command_execution_authorized":false,"allow_is_not_direct_execution":true,"baseline_commit":"5204ef93c569ea5d200cd9d3c79631500e566c78","capability":"inspect","effect":"READ_ONLY","f4g_gate_required":true,"network_transport_present":false,"opus_runtime_binding":"DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT","schema":"aletheusos.mission-control-platform-read-model.v1","services":{"A3ye":{"adapter":{"direct_subsystem_execution":false,"id":"a3ye.repository-read-model.v1","kind":"REPOSITORY_READ_MODEL","network_transport":false,"version":"1.0.0"},"contract":{"adapter_id":"a3ye.repository-read-model.v1","capability":"inspect","effect":"READ_ONLY","id":"a3ye.inspect.v1","surface":"A3ye","version":"1.0.0"},"read_model":{"evidence_count":2,"health_semantics":"TRACKED_IMPLEMENTATION_EVIDENCE_NOT_PROCESS_LIVENESS","implementation_evidence":[{"bytes":862,"clean":true,"path":"aletheus/a3ye/council_bridge/cli.py","sha256":"c58ffcc9ca6e8f6926efc58ce8467fb09d0c4843f8b71c19ad1d6f3ea592211e","tracked":true},{"bytes":804,"clean":true,"path":"aletheus/a3ye/core/cli.py","sha256":"c4b1cc76f408c28cc41b23b90173a9f1cc2c4aed7fb0db89b49ab2347a0e0646","tracked":true}],"status":"AVAILABLE_FOR_INSPECTION"}},"Mammoth":{"adapter":{"direct_subsystem_execution":false,"id":"mammoth.repository-read-model.v1","kind":"REPOSITORY_READ_MODEL","network_transport":false,"version":"1.0.0"},"contract":{"adapter_id":"mammoth.repository-read-model.v1","capability":"inspect","effect":"READ_ONLY","id":"mammoth.inspect.v1","surface":"Mammoth","version":"1.0.0"},"read_model":{"evidence_count":2,"health_semantics":"TRACKED_IMPLEMENTATION_EVIDENCE_NOT_PROCESS_LIVENESS","implementation_evidence":[{"bytes":13748,"clean":true,"path":"aletheus/institutional_civilization/civilization_catalog.py","sha256":"db6d4edf6562427964bc65b2c0720068c087b29a283730002a87bf468889d8ce","tracked":true},{"bytes":18214,"clean":true,"path":"aletheus/institutional_civilization/catalog.py","sha256":"3068c05a3944ebe80c01fda1d3dcb4170698851eb02c203f253edd17ad2524f8","tracked":true}],"status":"AVAILABLE_FOR_INSPECTION"}},"Platform Services":{"adapter":{"direct_subsystem_execution":false,"id":"platform-services.repository-read-model.v1","kind":"REPOSITORY_READ_MODEL","network_transport":false,"version":"1.0.0"},"contract":{"adapter_id":"platform-services.repository-read-model.v1","capability":"inspect","effect":"READ_ONLY","id":"platform-services.inspect.v1","surface":"Platform Services","version":"1.0.0"},"read_model":{"evidence_count":3,"health_semantics":"TRACKED_IMPLEMENTATION_EVIDENCE_NOT_PROCESS_LIVENESS","implementation_evidence":[{"bytes":35903,"clean":true,"path":"aletheus/runtime/core.py","sha256":"7c77c2f43dac57ff5c9c8b8d3203d450315caadc01f89712c3135590db5d094c","tracked":true},{"bytes":628,"clean":true,"path":"aletheus/platform/contracts/service.py","sha256":"75df703ac9f015b81ad75ae22bcd0911d7556dc5c945b144dee3e47d240c9b77","tracked":true},{"bytes":6681,"clean":true,"path":"tools/runtime_backbone.py","sha256":"6d0b62f9b9b44cdf143b04dfb28a7a39eb7562f5a10e3536c0fa606bae68a7f7","tracked":true}],"status":"AVAILABLE_FOR_INSPECTION"}}},"unknown_contract_adapter_or_service_refuses":true,"write_or_mutating_execution_authorized":false};

  const freeze = (value) => {
    if (!value || typeof value !== "object" || Object.isFrozen(value)) return value;
    Object.freeze(value);
    Object.values(value).forEach(freeze);
    return value;
  };

  freeze(PLATFORM_READ_MODEL);

  const contracts = freeze(
    Object.fromEntries(
      Object.entries(PLATFORM_READ_MODEL.services).map(([surface, service]) => [
        surface,
        { ...service.contract },
      ]),
    ),
  );

  const adapters = freeze(
    Object.fromEntries(
      Object.entries(PLATFORM_READ_MODEL.services).map(([surface, service]) => [
        surface,
        {
          ...service.adapter,
          inspect: () =>
            freeze({
              surface,
              capability: "inspect",
              effect: "READ_ONLY",
              ...service.read_model,
            }),
        },
      ]),
    ),
  );

  let receiptSequence = 0;

  const decisionCode = (value) => {
    if (value === true) return "ALLOW";
    if (value === false || value == null) return "REFUSE";
    if (typeof value === "string") return value.toUpperCase();
    if (typeof value === "object") {
      if (value.allowed === true || value.ok === true) return "ALLOW";
      if (value.allowed === false || value.ok === false) return "REFUSE";
      for (const key of ["decision", "status", "verdict", "result"]) {
        if (typeof value[key] === "string") return value[key].toUpperCase();
      }
    }
    return "UNKNOWN";
  };

  const makeReceipt = (fields) =>
    freeze({
      schema: "aletheusos.mission-control-execution-receipt.v1",
      request_id: `mcpi-${++receiptSequence}`,
      release: RELEASE,
      parent_release: PARENT_RELEASE,
      ...fields,
    });

  const refuse = (surface, capability, reason, gateEvidence = null) =>
    makeReceipt({
      surface,
      capability,
      effect: "READ_ONLY",
      result_status: "REFUSED",
      reason,
      gate_evidence: gateEvidence,
      service_contract: null,
      adapter: null,
      evidence: null,
    });

  const evaluateF4G = (surface, capability) => {
    const gate = globalThis.AletheusOS_MC84F4G;
    if (!gate || typeof gate[F4G_METHOD] !== "function") {
      return { code: "REFUSE", evidence: null, reason: "F4G_GATE_UNAVAILABLE" };
    }

    let evidence;
    try {
      evidence = gate[F4G_METHOD]({ surface, capability });
    } catch (error) {
      return {
        code: "REFUSE",
        evidence: freeze({
          error_name: error && error.name ? error.name : "Error",
          error_message: error && error.message ? error.message : "F4G evaluation failed",
        }),
        reason: "F4G_GATE_ERROR",
      };
    }

    const code = decisionCode(evidence);
    return { code, evidence, reason: code === "ALLOW" ? null : "F4G_NOT_ALLOW" };
  };

  const execute = (request = {}) => {
    const surface = typeof request.surface === "string" ? request.surface.trim() : "";
    const capability = typeof request.capability === "string" ? request.capability.trim() : "";

    if (!surface || !capability) return refuse(surface, capability, "INVALID_REQUEST");

    const gate = evaluateF4G(surface, capability);
    if (gate.code !== "ALLOW") {
      return refuse(surface, capability, gate.reason || "F4G_NOT_ALLOW", gate.evidence);
    }

    const contract = contracts[surface];
    if (!contract) return refuse(surface, capability, "SERVICE_CONTRACT_NOT_FOUND", gate.evidence);
    if (contract.capability !== capability) {
      return refuse(surface, capability, "CAPABILITY_NOT_DECLARED_BY_CONTRACT", gate.evidence);
    }
    if (contract.effect !== "READ_ONLY") {
      return refuse(surface, capability, "MUTATING_EFFECT_NOT_AUTHORIZED", gate.evidence);
    }

    const adapter = adapters[surface];
    if (!adapter || adapter.id !== contract.adapter_id) {
      return refuse(surface, capability, "AUTHORIZED_ADAPTER_NOT_FOUND", gate.evidence);
    }
    if (capability !== "inspect" || typeof adapter.inspect !== "function") {
      return refuse(surface, capability, "BOUNDED_EXECUTOR_DOES_NOT_SUPPORT_CAPABILITY", gate.evidence);
    }

    return makeReceipt({
      surface,
      capability,
      effect: "READ_ONLY",
      result_status: "OK",
      reason: null,
      gate_evidence: gate.evidence,
      service_contract: freeze({ id: contract.id, version: contract.version }),
      adapter: freeze({ id: adapter.id, version: adapter.version, kind: adapter.kind }),
      evidence: adapter.inspect(),
    });
  };

  const inspect = (surface) => execute({ surface, capability: "inspect" });

  const snapshot = () =>
    freeze({
      release: RELEASE,
      parent_release: PARENT_RELEASE,
      architecture: "CONSTITUTIONAL_PLATFORM_EXECUTION_BRIDGE",
      tranche: "CONSTITUTIONAL_PLATFORM_READ_MODEL_BRIDGE",
      initial_capability: "inspect",
      initial_effect: "READ_ONLY",
      f4g_gate_required: true,
      allow_is_not_direct_execution: true,
      network_transport_present: false,
      write_or_mutating_capabilities_authorized: false,
      a3ye_general_command_execution_authorized: false,
      opus_runtime_binding: "DEFERRED_PENDING_CONCRETE_RUNTIME_CONTRACT",
      services: Object.keys(PLATFORM_READ_MODEL.services),
      baseline_commit: PLATFORM_READ_MODEL.baseline_commit,
    });

  globalThis.AletheusOS_MC_PLATFORM_INTEGRATION = freeze({
    release: RELEASE,
    architecture: "CONSTITUTIONAL_PLATFORM_EXECUTION_BRIDGE",
    tranche: "CONSTITUTIONAL_PLATFORM_READ_MODEL_BRIDGE",
    contracts,
    execute,
    inspect,
    snapshot,
  });
})();
