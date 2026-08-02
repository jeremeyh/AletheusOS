import * as THREE from "three";
export class ThreeSwapCanvasEngine {
  private currentTheta=0; private targetTheta=0; private velocity=0;
  public update(left:number,right:number):void { this.targetTheta=-0.35*Math.tanh((left-right)/200.0); }
  public tick(dt:number):number { const k=120,m=1,z=0.85,c=2*z*Math.sqrt(k*m); const a=(-k*(this.currentTheta-this.targetTheta)-c*this.velocity)/m; this.velocity+=a*dt; this.currentTheta+=this.velocity*dt; return this.currentTheta; }
}
