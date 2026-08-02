use wasm_bindgen::prelude::*;
#[wasm_bindgen] pub struct SpatialNodeSpring { p:[f32;3], t:[f32;3], v:[f32;3], k:f32, z:f32, m:f32 }
#[wasm_bindgen] impl SpatialNodeSpring {
#[wasm_bindgen(constructor)] pub fn new(x:f32,y:f32,z:f32,k:f32,d:f32)->Self{Self{p:[x,y,z],t:[x,y,z],v:[0.0;3],k:k.max(0.0),z:d.max(0.0),m:1.0}}
pub fn set_target(&mut self,x:f32,y:f32,z:f32){self.t=[x,y,z]}
pub fn update(&mut self,dt:f32){let n=4;let h=dt.clamp(0.0,0.032)/n as f32;let c=2.0*self.z*(self.k*self.m).sqrt();for _ in 0..n{for i in 0..3{let a=(-self.k*(self.p[i]-self.t[i])-c*self.v[i])/self.m;self.v[i]+=a*h;self.p[i]+=self.v[i]*h;}}}
pub fn x(&self)->f32{self.p[0]} pub fn y(&self)->f32{self.p[1]} pub fn z(&self)->f32{self.p[2]}
}