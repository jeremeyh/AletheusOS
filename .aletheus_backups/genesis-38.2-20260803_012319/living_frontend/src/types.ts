export type PhaseState = "Nebular" | "Fluid Reactive" | "Quasi-Crystalline" | "Crystalline Solid";
export interface InstrumentDefinition { id:string; title:string; metric:string; value:number; accent:string; detail:string; risk:"stable"|"watch"|"strong"; }
