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
