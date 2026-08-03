use serde::Serialize;
use wasm_bindgen::prelude::*;
#[derive(Serialize)] struct Resonance{gain:f64,damped_hz:f64,practical:f64,harmonic_energy:f64}
#[wasm_bindgen]
pub fn evaluate(natural:f64,driving:f64,zeta:f64,coupling:f64,coherence:f64,vitality:f64,latency:f64,target:f64)->Result<JsValue,JsValue>{
 let r=driving/natural.max(1e-9);
 let d=((1.0-r*r).powi(2)+(2.0*zeta*r).powi(2)).sqrt().max(1e-9);
 let gain=coupling/d;
 let damped=natural*(1.0-zeta.clamp(0.0,0.999999).powi(2)).sqrt();
 let practical=((0.55*coherence.clamp(0.0,1.0)+0.45*vitality.clamp(0.0,1.0))*target/latency.max(target)).clamp(0.0,1.0);
 serde_wasm_bindgen::to_value(&Resonance{gain,damped_hz:damped,practical,harmonic_energy:(gain*practical).tanh()}).map_err(Into::into)
}
