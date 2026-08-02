export interface SpringConfig { stiffness:number; dampingRatio:number; mass:number }
export interface ScalarSpringState { current:number; target:number; velocity:number }
export function stepSpring(s:ScalarSpringState,c:SpringConfig,dt:number):ScalarSpringState { const n=5; const h=Math.min(Math.max(dt,0),.032)/n; let x=s.current,v=s.velocity; const d=2*c.dampingRatio*Math.sqrt(c.stiffness*c.mass); for(let i=0;i<n;i++){const f=-c.stiffness*(x-s.target)-d*v; v+=(f/c.mass)*h; x+=v*h;} return {current:x,target:s.target,velocity:v}; }
