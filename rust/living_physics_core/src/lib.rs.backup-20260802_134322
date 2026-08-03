use serde::{Deserialize,Serialize};
use wasm_bindgen::prelude::*;
#[derive(Deserialize,Serialize)]
struct Body{x:f32,y:f32,z:f32,vx:f32,vy:f32,vz:f32,mass:f32,confidence:f32,urgency:f32,contradiction:f32}
#[derive(Deserialize)]
struct Field{gravity:f32,elasticity:f32,viscosity:f32,turbulence:f32}
fn c(v:f32)->f32{v.clamp(0.0,1.0)}
#[wasm_bindgen]
pub fn step_body(body:JsValue,tx:f32,ty:f32,tz:f32,field:JsValue,dt:f32)->Result<JsValue,JsValue>{
 let mut b:Body=serde_wasm_bindgen::from_value(body)?;
 let f:Field=serde_wasm_bindgen::from_value(field)?;
 let h=dt.clamp(0.0,0.032)/4.0;
 let stress=.55*c(b.urgency)+.45*c(b.contradiction);
 let e=(f.elasticity*(.65+.35*c(b.confidence))*(1.0-.55*stress)).max(.05);
 let g=f.gravity*b.mass.max(0.0)*(.5+.5*c(b.confidence));
 for _ in 0..4{
  let dx=-f.viscosity*b.vx-f.turbulence*b.vx*b.vx.abs();
  let dy=-f.viscosity*b.vy-f.turbulence*b.vy*b.vy.abs();
  let dz=-f.viscosity*b.vz-f.turbulence*b.vz*b.vz.abs();
  b.vx+=(e*(tx-b.x)+dx)*h; b.vy+=(e*(ty-b.y)+dy)*h; b.vz+=(e*(tz-b.z)+dz-g*.0005)*h;
  b.x+=b.vx*h; b.y+=b.vy*h; b.z+=b.vz*h;
 }
 serde_wasm_bindgen::to_value(&b).map_err(Into::into)
}
