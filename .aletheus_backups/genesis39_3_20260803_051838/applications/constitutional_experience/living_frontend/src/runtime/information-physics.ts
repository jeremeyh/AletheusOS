import type { PhaseState, TelemetryState } from "../types";
export const clamp01=(v:number)=>Math.max(0,Math.min(1,v));
export function constitutionalResonance(v:number,c:number,k:number){const gate=c>=0.94&&k<=0.08?1:0;return clamp01((v*0.5+c*0.5)*gate);}
export function phaseForDensity(d:number):PhaseState{if(d<0.35)return "Nebular";if(d<0.70)return "Fluid Reactive";if(d<0.92)return "Quasi-Penrose";return "Crystalline Solid";}
export function meantimeQuotient(progress:number,seconds:number,coherence:number,vitality:number){return clamp01((progress/Math.max(seconds,1))*(0.55*clamp01(coherence)+0.45*clamp01(vitality)));}
export const defaultTelemetry:TelemetryState={veracity:0.982,consensus:0.947,contradiction:0.061,elasticity:0.72,resonance:0.965,fieldDensity:0.72,entropy:0.17,missionMass:0.86,founderMode:0,meantimeQuotient:0.913};
