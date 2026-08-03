import type { RuntimeSignal } from "../types.js";
import { informationMass, veracityPhase } from "../runtime/math.js";

const signals: RuntimeSignal[] = [
  { id:"truth",label:"Truth Confidence",value:96,confidence:.96,urgency:.22,contradiction:.08,provenance:.98,consensus:.94 },
  { id:"mission",label:"Mission Continuity",value:88,confidence:.89,urgency:.38,contradiction:.14,provenance:.91,consensus:.87 },
  { id:"security",label:"Security Posture",value:92,confidence:.93,urgency:.31,contradiction:.06,provenance:.95,consensus:.9 },
];

function meter(label:string,value:number,phase:string):string { return `<div class="meter"><div class="meter-row"><span>${label}</span><strong>${value.toFixed(0)}</strong></div><div class="meter-track"><i class="phase-${phase}" style="width:${Math.min(100,value)}%"></i></div></div>`; }

export function renderInstrument(id:string):string {
  switch(id){
    case "mission-health": return `<div class="instrument-copy"><p class="eyebrow">Autonomous Mission Runtime™</p><h3>Mission field is coherent</h3>${signals.map(s=>meter(s.label,s.value,veracityPhase(s.confidence))).join("")}<div class="status-strip"><span>7 active</span><span>0 blocked</span><span>2 awaiting authority</span></div></div>`;
    case "runtime-topology": return `<div class="topology"><div class="topology-core">CRK™</div>${["A•3ye™","SPAN™","SPARTAN™","Mammoth™","Nimble™","Kinekt™"].map((x,i)=>`<div class="topology-node n${i}">${x}</div>`).join("")}<svg viewBox="0 0 500 260" aria-hidden="true"><g>${[[250,130,80,45],[250,130,420,45],[250,130,70,205],[250,130,430,205],[250,130,250,20],[250,130,250,240]].map(a=>`<line x1="${a[0]}" y1="${a[1]}" x2="${a[2]}" y2="${a[3]}"/>`).join("")}</g></svg></div>`;
    case "information-physics": return `<div><p class="eyebrow">Semantic Gravity</p>${signals.map(s=>meter(`${s.label} · mass ${informationMass(s).toFixed(1)}`,s.confidence*100,veracityPhase(s.confidence))).join("")}<div class="phase-legend"><span>Nebular</span><span>Fluid</span><span>Quasi</span><span>Crystalline</span></div></div>`;
    case "constitutional-compliance": return `<div class="compliance-ring"><div><strong>98.7</strong><span>Constitutional Index</span></div></div><ul class="clean-list"><li>Truth provenance verified</li><li>Human authority preserved</li><li>Founder plane isolated</li><li>No boundary drift detected</li></ul>`;
    case "spartan-posture": return `<div class="instrument-copy"><p class="eyebrow">SPARTAN™</p><h3>Defensive lattice stable</h3>${meter("Containment readiness",94,"crystalline")}${meter("Identity assurance",97,"crystalline")}${meter("Threat ambiguity",21,"nebular")}</div>`;
    case "market-intelligence": return `<div class="instrument-copy"><p class="eyebrow">Card Hawk™</p><h3>Opportunity field</h3><div class="market-grid"><b>+18.4%</b><span>scarcity momentum</span><b>0.82</b><span>market conviction</span><b>12</b><span>priority signals</span></div></div>`;
    case "founder-observatory": return `<div class="founder-view"><p class="eyebrow">Founder Root Plane</p><h3>Eye in the sky</h3><div class="founder-grid"><div><b>18,402</b><span>active user journeys</span></div><div><b>4,218</b><span>transactions observed</span></div><div><b>27</b><span>developer contributions</span></div><div><b>99.94%</b><span>platform health</span></div></div><p class="founder-warning">Visibility is broad; authority remains explicit, attributable, and constitutionally bounded.</p></div>`;
    default: return `<p>Instrument unavailable.</p>`;
  }
}
