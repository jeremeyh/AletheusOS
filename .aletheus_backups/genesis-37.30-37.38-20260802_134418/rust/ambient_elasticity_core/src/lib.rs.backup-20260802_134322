use wasm_bindgen::prelude::*;
#[wasm_bindgen] pub fn elasticity(base:f64,confidence:f64,urgency:f64,contradiction:f64)->f64{
 let stress=.55*urgency.clamp(0.0,1.0)+.45*contradiction.clamp(0.0,1.0);
 (base*(.65+.35*confidence.clamp(0.0,1.0))*(1.0-.55*stress)).max(.05)
}
#[wasm_bindgen] pub fn manifold(distance:f64,curvature:f64)->f64{((if curvature==0.0{1.0}else{curvature.abs().sqrt()})*distance.max(0.0)).tanh()}
#[wasm_bindgen] pub fn breathe(t:f64,hz:f64)->f64{.5+.5*(std::f64::consts::TAU*hz*t).sin()}
