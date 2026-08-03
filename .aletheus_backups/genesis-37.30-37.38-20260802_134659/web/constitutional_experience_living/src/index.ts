export interface LivingState { vitality:number; coherence:number; resonance:number; elasticity:number; meantimeQuotient:number; phase:string }
export class LivingRuntime {
  state: LivingState={vitality:.5,coherence:.5,resonance:.5,elasticity:.6,meantimeQuotient:1,phase:"nebular"};
  breathe(t:number,hz=.15){return .5+.5*Math.sin(2*Math.PI*hz*t)}
  update(next:Partial<LivingState>){this.state={...this.state,...next};return structuredClone(this.state)}
}
export class WorkspaceComposer {
  private registry=new Map<string,{id:string;founderOnly?:boolean}>(); private layout:unknown[]=[];
  register(i:{id:string;founderOnly?:boolean}){if(i.founderOnly)throw new Error("Founder boundary");this.registry.set(i.id,structuredClone(i))}
  save(storage:Storage,key:string){storage.setItem(key,JSON.stringify(this.layout))}
}
export class FounderObservatory {
  #ok=false;
  attest(proof:string){if(proof.length<48)throw new Error("Root proof rejected");this.#ok=true}
  synthesize<T>(data:T):T{if(!this.#ok)throw new Error("Founder root required");return structuredClone(data)}
}
