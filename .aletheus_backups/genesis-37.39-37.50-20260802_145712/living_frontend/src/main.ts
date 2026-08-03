import { mountComposer } from "./workspace/composer.js";
import { resolvePrincipal, canAccessFounderObservatory } from "./security/principal.js";
import { initializeWasmRuntime } from "./runtime/wasmBridge.js";
import { startRenderer } from "./runtime/webgpu.js";
import { meantimeQuotient, respiration } from "./runtime/math.js";

const principal=resolvePrincipal();
const app=document.querySelector<HTMLDivElement>("#app");
if(!app)throw new Error("Application mount missing");
app.innerHTML=`
<canvas id="field-canvas"></canvas>
<div class="ambient-orb orb-a"></div><div class="ambient-orb orb-b"></div>
<header class="topbar"><div class="brand"><div class="brand-mark">A</div><div><b>ALETHEUS<span>OS</span></b><small>Living Constitutional Experience</small></div></div><nav><button class="nav-active">Mission Field</button><button data-open-library>Workspace Composer</button>${canAccessFounderObservatory(principal)?'<button>Founder Observatory</button>':''}</nav><div class="operator"><span class="pulse-dot"></span><div><b>${principal.displayName}</b><small>${principal.claims.includes("founder_root")?"Founder Root":"Constitutional Operator"}</small></div></div></header>
<aside id="library" class="library" hidden><header><div><p class="eyebrow">Instrument Registry</p><h2>Compose workspace</h2></div><button data-open-library>×</button></header><div id="library-list" class="library-list"></div><button data-reset class="secondary-action">Restore canonical layout</button></aside>
<main><section class="hero"><div><p class="eyebrow">Genesis 37.39–37.50</p><h1>The intelligence field is <em>alive.</em></h1><p>Information reorganizes around mission, evidence, confidence, and human authority.</p></div><div class="runtime-badges"><span id="renderer-badge">Renderer: awakening</span><span id="wasm-badge">WASM: awakening</span><span id="mq-badge">MQ: calibrating</span></div></section><section id="workspace" class="workspace" aria-label="Living workspace"></section></main>
<footer><span>Truth-bound · Human-authorized · Constitutionally observable</span><span id="clock"></span></footer>`;

const canvas=document.querySelector<HTMLCanvasElement>("#field-canvas")!;
let phase=0.72;
startRenderer(canvas,()=>phase).then(status=>{document.querySelector("#renderer-badge")!.textContent=`Renderer: ${status.mode.toUpperCase()}`;});
initializeWasmRuntime().then(state=>{document.querySelector("#wasm-badge")!.textContent=state.available?"WASM: 3/3 ONLINE":`WASM: fallback (${3-state.errors.length}/3)`;});
mountComposer(document.querySelector<HTMLElement>("#workspace")!,principal);
let last=performance.now();
const animate=(now:number)=>{const dt=now-last;last=now;const breath=respiration(now/1000);phase=.62+.22*breath;document.documentElement.style.setProperty("--breath",String(breath));document.querySelector("#mq-badge")!.textContent=`MQ: ${meantimeQuotient(dt,.94,.91).toFixed(3)}`;requestAnimationFrame(animate)};requestAnimationFrame(animate);
setInterval(()=>{document.querySelector("#clock")!.textContent=new Date().toLocaleTimeString([], {hour:"2-digit",minute:"2-digit",second:"2-digit"});},1000);
