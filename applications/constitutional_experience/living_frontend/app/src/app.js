const domains=[['■','Mission Control','Missions & executive overview'],['▦','Workspace Studio','Workspaces & execution'],['⌘','Builder Studio','Platform engineering'],['>_','Admin Terminal','System & governance'],['⬡','Platform Services','Core services & integrations'],['⌁','Analytics Studio','Insights & telemetry'],['◇','Opus','Knowledge civilization'],['◉','Mammoth','Storage civilization'],['♙','Organizations','Teams & tenants'],['⬢','Security','Policy & compliance']];
const missions=[['M-001','AletheusOS Platform Realization','ACTIVE','78%'],['M-002','Card Hawk Asset Vault','ACTIVE','64%'],['M-003','SPARTAN Security Convergence','WATCH','41%'],['M-004','Mammoth Storage Federation','PLANNED','18%']];
const activity=[['10:54:32','Mission Control hydrated','System'],['10:54:11','Opus knowledge graph synchronized','Opus'],['10:53:47','CRK kernel heartbeat verified','Runtime'],['10:53:19','Builder Studio project compiled','Builder'],['10:52:58','Evidence pipeline completed','A🔘3ye']];
const app=document.querySelector('#app');
const lens=(id,cls='')=>`<button id="${id}" class="a3ye-lens ${cls}" aria-label="Open A🔘3ye perception"><span class="lens-cradle" aria-hidden="true"></span><span class="orbit orbit-a"></span><span class="orbit orbit-b"></span><span class="lens-glass"><img src="./assets/a3ye-universal-lens.jpeg" alt="A🔘3ye universal lens"><span class="scan"></span><span class="core"></span></span><span class="aos3-cardinals" aria-hidden="true"><i class="cardinal cardinal-a">A</i><i class="cardinal cardinal-o">O</i><i class="cardinal cardinal-s">S</i><i class="cardinal cardinal-3">3</i></span></button>`;
app.innerHTML=`<div class="shell">
<header class="topbar">
<div class="brand"><button class="brand-mark" aria-label="AletheusOS home"><img src="./assets/aletheus-gold-mark.jpeg" alt="AletheusOS gold mark"></button><div><b>ALETHEUSOS</b><span>GENESIS 84.0.0</span></div></div>
<div class="context"><b>Mission Control</b><span>Constitutional Instrument Runtime</span></div>
<div class="command-surface">${lens('lensTop','top-lens command-lens')}<button id="command" class="search"><span class="search-glyph">⌕</span><span>Ask A🔘3ye or type a command...</span><kbd>⌘K</kbd></button></div>
<div class="tools"><button title="Connectors">♧</button><button title="Theme">☼</button><button title="Help">?</button></div>
<div class="founder"><button id="founderAvatar" class="founder-avatar" type="button" aria-label="Upload Founder profile picture"><span class="founder-silhouette" aria-hidden="true"><svg viewBox="0 0 48 48" role="img"><circle cx="24" cy="16" r="8"></circle><path d="M10 41c1.2-9 6.8-14 14-14s12.8 5 14 14"></path></svg></span><img id="founderPhoto" alt="Founder profile" hidden></button><input id="founderPhotoInput" type="file" accept="image/*" hidden><div class="founder-copy"><b>Founder⌄</b><span>6DM</span></div></div>
</header>
<aside class="sidebar"><label>OPERATING DOMAINS</label><nav>${domains.map((d,i)=>`<button class="domain ${i===0?'active':''}"><i>${d[0]}</i><span><b>${d[1]}</b><small>${d[2]}</small></span></button>`).join('')}</nav><div class="sys"><span>System Status</span><b>● OPERATIONAL</b></div></aside>
<main class="main"><div class="section-head"><div><label>MISSION CONTROL</label><h1>Platform Command Surface</h1></div><div class="view-actions"><button>Object Explorer</button><button>Runtime Map</button><button>Timeline</button></div></div>
<section class="metrics">${[['Active Missions','4','● 3 executing'],['Constitutional Integrity','VERIFIED','No violations'],['Qₘ Stability','91.4','NOMINAL'],['Runtime Health','OPTIMAL','All systems nominal'],['Evidence Items','127','Total collected']].map((m,i)=>`<article><small>${m[0]}</small><strong class="${i===1||i===3?'green':''}">${m[1]}</strong><span>${m[2]}</span></article>`).join('')}</section>
<section class="primary-grid"><article class="panel"><h3>ACTIVE MISSIONS</h3>${missions.map(m=>`<div class="mission"><span>${m[0]}</span><b>${m[1]}</b><em class="${m[2].toLowerCase()}">${m[2]}</em><strong>${m[3]}</strong></div>`).join('')}<a>Open Mission Center →</a></article><article class="panel"><h3>A🔘3ye RECOMMENDATIONS</h3>${['Promote Mission Control as default landing surface','Reconcile duplicate Workspace Runtime adapters','Pin SPARTAN readiness review to today'].map((x,i)=>`<div class="recommend"><i>0${i+1}</i><span><b>${x}</b><small>Confidence ${94-i*6}% · Evidence-backed</small></span></div>`).join('')}<a>Review all recommendations →</a></article></section>
<section class="secondary-grid"><article class="panel"><h3>RECENT INTELLIGENCE</h3>${activity.map(a=>`<div class="row"><i>◈</i><time>${a[0]}</time><b>${a[1]}</b><span>${a[2]}</span></div>`).join('')}<a>View all activity →</a></article><article class="panel"><h3>RUNTIME TELEMETRY</h3><div class="telegrid">${['CPU|18%','Memory|42%','GPU|22%','Qₘ Stability|91.4','FPS|60','Threads|128'].map((t,i)=>{const [l,v]=t.split('|');return`<div><small>${l}</small><b>${v}</b><svg viewBox="0 0 100 30"><polyline points="0,27 12,24 25,25 38,18 50,20 62,12 75,14 88,7 100,8"/></svg></div>`}).join('')}</div><a>Open Runtime Visualization →</a></article></section>
<section id="instrumentBay" class="panel instrument-bay"><div class="instrument-title"><div><label>CONSTITUTIONAL INSTRUMENT BAY</label><h2>Calibrate Runtime Observability</h2></div><span class="quality-badge">EVIDENCE-BOUND · GENESIS 84</span></div><div class="instrument-grid">
<button class="instrument integrity-ring" data-instrument="Integrity Ring"><span class="dial"><i></i><b>100</b><small>%</small></span><strong>Integrity Ring</strong><em>VERIFIED</em><footer data-source="CRK integrity stream">CRK · sampled 0.4s ago</footer></button>
<button class="instrument runtime-pulse" data-instrument="Runtime Pulse"><span class="pulse-field"><i></i><i></i><i></i><b>72</b></span><strong>Runtime Pulse</strong><em>NOMINAL BPM</em><footer data-source="CRK scheduler heartbeat">Scheduler · sampled 0.2s ago</footer></button>
<button class="instrument evidence-flow" data-instrument="Evidence Flow"><span class="flow-meter"><i style="height:26%"></i><i style="height:48%"></i><i style="height:66%"></i><i style="height:82%"></i><i style="height:58%"></i><i style="height:74%"></i><i style="height:91%"></i><i style="height:68%"></i></span><strong>Evidence Flow</strong><em>127 ITEMS · 8.4/s</em><footer data-source="Evidence Engine event stream">Evidence Engine · sampled 0.8s ago</footer></button>
<button class="instrument consensus-field" data-instrument="Consensus Field"><span class="radar"><i></i><b>88</b></span><strong>Consensus Field</strong><em>HIGH AGREEMENT</em><footer data-source="Reasoning mesh consensus">Reason Mesh · derived 1.1s ago</footer></button>
<button class="instrument risk-horizon" data-instrument="Risk Horizon"><span class="horizon"><i></i><b>0.18</b></span><strong>Risk Horizon</strong><em>LOW EXPOSURE</em><footer data-source="Risk Engine projection">Risk Engine · forecast 2.0s ago</footer></button>
<button class="instrument qm-instrument" data-instrument="Qm Stability"><span class="qm-scope"><svg viewBox="0 0 160 70"><polyline points="0,44 14,42 28,46 42,35 56,38 70,28 84,31 98,20 112,24 126,15 140,18 160,11"/></svg><b>91.4</b></span><strong>Qₘ Stability</strong><em>NOMINAL</em><footer data-source="Temporal isolation monitor">Temporal Monitor · sampled 0.3s ago</footer></button>
</div></section>
<section class="workspace-strip"><article class="panel"><h3>WORKSPACE DIRECTORY</h3><div class="tiles"><div>▦ <span>Sentinel Operations<small>Active now</small></span></div><div>⬡ <span>Evidence Review<small>Active 5h ago</small></span></div><div>⌘ <span>Builder Studio<small>Pinned</small></span></div><div>◇ <span>Opus Knowledge<small>Pinned</small></span></div></div></article><article class="panel attention"><h3>ATTENTION QUEUE</h3><div><b>2</b><span>Evidence items awaiting review</span></div><div><b>1</b><span>Security policy drift warning</span></div><div><b>3</b><span>Mission dependencies pending</span></div></article></section></main>
<div id="drawerScrim" class="drawer-scrim"></div><aside id="drawer" class="drawer"><div class="drawer-head"><div>${lens('lensDrawer','drawer-lens')}<span><b>A🔘3ye Perception</b><small>Constitutional Perception Platform</small></span></div><button id="closeDrawer">×</button></div><div class="ask"><input placeholder="Ask a question or request analysis..."><button>➤</button></div><div class="tabs"><b>Recent</b><span>Suggested</span><span>Workspaces</span></div><div class="prompts">${['What missions need attention?','Verify system health and integrity','Show recent evidence collected','Explain current Qₘ stability','List available platform services'].map((p,i)=>`<button><span>${p}</span><time>10:${54-i} AM</time></button>`).join('')}</div><label>CAPABILITIES</label><div class="caps">${['Ask','Verify','Examine','Analyze','Forecast'].map((c,i)=>`<button><i>${['◌','⬡','⌕','△','↗'][i]}</i><span>${c}</span></button>`).join('')}</div><footer>● A🔘3ye is observing. Truth backed by SIGHT.</footer></aside>
<aside id="instrumentInspector" class="instrument-inspector"><button id="closeInstrument">×</button><label>INSTRUMENT INSPECTION</label><h2 id="instrumentName">Integrity Ring</h2><div class="inspector-value"><strong id="instrumentValue">100%</strong><span id="instrumentState">VERIFIED</span></div><dl><div><dt>QUALITY</dt><dd>SIMULATED</dd></div><div><dt>SOURCE</dt><dd id="instrumentSource">CRK integrity stream</dd></div><div><dt>FRESHNESS</dt><dd>Under 2 seconds</dd></div><div><dt>CALIBRATION</dt><dd>Genesis 62–82 production profile</dd></div></dl><p>Values in this standalone package are simulated and must not be interpreted as live platform measurements. Runtime adapters will replace this source without changing the visual contract.</p></aside>
<footer class="bottom"><div class="dock"><button title="Finder">▰</button><button title="Opus">◇</button><button title="Terminal">>_</button><button title="Runtime">⌁</button><button title="Settings">⚙</button></div><div class="runtime"><b>● CRK CONVERGED</b><span>Integrity<strong>VERIFIED</strong></span><span>Scheduler<strong>Optimal</strong></span><span>Threads<strong>128</strong></span><span>FPS<strong>60</strong></span><span>Qₘ<strong id="qm">91.4</strong></span><time id="clock"></time></div></footer>
</div><div id="palette" class="overlay hidden"><section><header><span>⌕</span><input placeholder="Type a command or ask A🔘3ye..."><button id="closePalette">ESC</button></header>${['Open Mission Control','Open Builder Studio','Search Evidence','Ask A🔘3ye','Compile Project','Run Tests','Open Card Hawk','Launch SPARTAN'].map(x=>`<button>${x}</button>`).join('')}</section></div>`;
const drawer=document.querySelector('#drawer'),scrim=document.querySelector('#drawerScrim');
function openDrawer(){drawer.classList.add('open');scrim.classList.add('open');document.body.classList.add('perception-open')}
function closeDrawer(){drawer.classList.remove('open');scrim.classList.remove('open');document.body.classList.remove('perception-open')}
function toggleDrawer(){drawer.classList.contains('open')?closeDrawer():openDrawer()}
document.querySelector('#lensTop').onclick=toggleDrawer;document.querySelector('#closeDrawer').onclick=closeDrawer;scrim.onclick=closeDrawer;
const palette=document.querySelector('#palette');document.querySelector('#command').onclick=()=>palette.classList.remove('hidden');document.querySelector('#closePalette').onclick=()=>palette.classList.add('hidden');
window.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();palette.classList.remove('hidden')}if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='j'){e.preventDefault();toggleDrawer()}if(e.key==='Escape'){palette.classList.add('hidden');closeDrawer()}});
const founderAvatar=document.querySelector('#founderAvatar'),founderPhotoInput=document.querySelector('#founderPhotoInput'),founderPhoto=document.querySelector('#founderPhoto');
founderAvatar.onclick=()=>founderPhotoInput.click();
founderPhotoInput.addEventListener('change',()=>{const file=founderPhotoInput.files&&founderPhotoInput.files[0];if(!file)return;const reader=new FileReader();reader.onload=()=>{founderPhoto.src=String(reader.result);founderPhoto.hidden=false;founderAvatar.classList.add('has-photo');try{localStorage.setItem('aletheus-founder-photo',String(reader.result))}catch{}};reader.readAsDataURL(file)});
try{const savedPhoto=localStorage.getItem('aletheus-founder-photo');if(savedPhoto){founderPhoto.src=savedPhoto;founderPhoto.hidden=false;founderAvatar.classList.add('has-photo')}}catch{}
const inspector=document.querySelector('#instrumentInspector');
const valueMap={'Integrity Ring':['100%','VERIFIED'],'Runtime Pulse':['72','NOMINAL BPM'],'Evidence Flow':['127','8.4 ITEMS/S'],'Consensus Field':['88%','HIGH AGREEMENT'],'Risk Horizon':['0.18','LOW EXPOSURE'],'Qm Stability':['91.4','NOMINAL']};
document.querySelectorAll('[data-instrument]').forEach(el=>el.addEventListener('click',()=>{const name=el.dataset.instrument;const [value,state]=valueMap[name]||['—','UNAVAILABLE'];document.querySelector('#instrumentName').textContent=name;document.querySelector('#instrumentValue').textContent=value;document.querySelector('#instrumentState').textContent=state;document.querySelector('#instrumentSource').textContent=el.querySelector('footer').dataset.source;inspector.classList.add('open')}));
document.querySelector('#closeInstrument').onclick=()=>inspector.classList.remove('open');
setInterval(()=>{document.querySelector('#qm').textContent=(91.4+(Math.random()*.2-.1)).toFixed(1)},1500);setInterval(()=>{document.querySelector('#clock').textContent=new Date().toLocaleTimeString([],{hour:'numeric',minute:'2-digit'})},1000);

/* ==========================================================================
   ALETHEUSOS MC85E2 — CURRENT RUNTIME CONVERGENCE CANDIDATE
   Visual authority above this boundary remains MC85E2.
   Runtime bridge below is transplanted from the current functional donor.
   ========================================================================== */

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
