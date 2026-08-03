import { instruments } from "../data/instruments.js";
import type { Principal, WorkspaceInstrument, WorkspaceState } from "../types.js";
import { canAccessFounderObservatory } from "../security/principal.js";
import { renderInstrument } from "../components/instrumentViews.js";

const KEY="aletheus.genesis37.workspace.v1";
const defaultState:WorkspaceState={version:1,name:"Living Mission Field",instruments:[
  {instanceId:"mission-1",instrumentId:"mission-health",x:24,y:24,width:420,height:280},
  {instanceId:"topology-1",instrumentId:"runtime-topology",x:468,y:24,width:560,height:360},
  {instanceId:"physics-1",instrumentId:"information-physics",x:24,y:328,width:420,height:300},
  {instanceId:"compliance-1",instrumentId:"constitutional-compliance",x:468,y:408,width:420,height:280},
]};

function load():WorkspaceState{try{const raw=localStorage.getItem(KEY);return raw?JSON.parse(raw) as WorkspaceState:structuredClone(defaultState);}catch{return structuredClone(defaultState)}}
function save(state:WorkspaceState){localStorage.setItem(KEY,JSON.stringify(state));}

export function mountComposer(host:HTMLElement,principal:Principal):void{
 let state=load();
 const render=()=>{
  host.innerHTML="";
  for(const item of state.instruments){
   const def=instruments.find(x=>x.id===item.instrumentId); if(!def)continue;
   if(def.founderOnly&&!canAccessFounderObservatory(principal))continue;
   const el=document.createElement("article");el.className="instrument";el.dataset.instanceId=item.instanceId;
   el.style.transform=`translate(${item.x}px,${item.y}px)`;el.style.width=`${item.width}px`;el.style.height=`${item.height}px`;
   el.innerHTML=`<header><span>${def.title}</span><button data-remove aria-label="Remove">×</button></header><section>${renderInstrument(def.id)}</section><div class="resize-handle" aria-hidden="true"></div>`;
   host.append(el); wireDrag(el,item); wireResize(el,item);
   el.querySelector("[data-remove]")?.addEventListener("click",()=>{state.instruments=state.instruments.filter(x=>x.instanceId!==item.instanceId);save(state);render();});
  }
 };
 const wireDrag=(el:HTMLElement,item:WorkspaceInstrument)=>{
  const handle=el.querySelector("header") as HTMLElement; let sx=0,sy=0,ox=0,oy=0;
  handle.addEventListener("pointerdown",e=>{if((e.target as HTMLElement).closest("button"))return;sx=e.clientX;sy=e.clientY;ox=item.x;oy=item.y;handle.setPointerCapture(e.pointerId);el.classList.add("moving")});
  handle.addEventListener("pointermove",e=>{if(!handle.hasPointerCapture(e.pointerId))return;item.x=Math.max(0,ox+e.clientX-sx);item.y=Math.max(0,oy+e.clientY-sy);el.style.transform=`translate(${item.x}px,${item.y}px)`;});
  handle.addEventListener("pointerup",e=>{handle.releasePointerCapture(e.pointerId);el.classList.remove("moving");save(state)});
 };
 const wireResize=(el:HTMLElement,item:WorkspaceInstrument)=>{const h=el.querySelector(".resize-handle") as HTMLElement;let sx=0,sy=0,ow=0,oh=0;h.addEventListener("pointerdown",e=>{sx=e.clientX;sy=e.clientY;ow=item.width;oh=item.height;h.setPointerCapture(e.pointerId)});h.addEventListener("pointermove",e=>{if(!h.hasPointerCapture(e.pointerId))return;item.width=Math.max(280,ow+e.clientX-sx);item.height=Math.max(200,oh+e.clientY-sy);el.style.width=`${item.width}px`;el.style.height=`${item.height}px`;});h.addEventListener("pointerup",e=>{h.releasePointerCapture(e.pointerId);save(state)});};
 document.querySelector("[data-open-library]")?.addEventListener("click",()=>{const panel=document.querySelector("#library") as HTMLElement;panel.hidden=!panel.hidden;});
 const library=document.querySelector("#library-list"); if(library){library.innerHTML="";for(const def of instruments){if(def.founderOnly&&!canAccessFounderObservatory(principal))continue;const b=document.createElement("button");b.innerHTML=`<strong>${def.title}</strong><span>${def.category}</span>`;b.addEventListener("click",()=>{state.instruments.push({instanceId:`${def.id}-${Date.now()}`,instrumentId:def.id,x:40+state.instruments.length*20,y:40+state.instruments.length*20,width:def.defaultWidth,height:def.defaultHeight});save(state);render();});library.append(b);}}
 document.querySelector("[data-reset]")?.addEventListener("click",()=>{state=structuredClone(defaultState);save(state);render();});
 render();
}
