use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn poincare_distance(px: f64, py: f64, pz: f64, qx: f64, qy: f64, qz: f64) -> f64 {
    let p2 = px*px + py*py + pz*pz;
    let q2 = qx*qx + qy*qy + qz*qz;
    if p2 >= 1.0 || q2 >= 1.0 { return f64::INFINITY; }
    let dx = px-qx; let dy = py-qy; let dz = pz-qz;
    let delta2 = dx*dx + dy*dy + dz*dz;
    (1.0 + 2.0*delta2 / ((1.0-p2)*(1.0-q2))).acosh()
}

#[wasm_bindgen]
pub fn project_to_ball(x: f64, y: f64, z: f64, curvature: f64) -> Box<[f64]> {
    let r = (x*x + y*y + z*z).sqrt();
    if r == 0.0 { return vec![0.0,0.0,0.0].into_boxed_slice(); }
    let c = curvature.abs().max(0.0001);
    let scale = (c.sqrt()*r).tanh() / (c.sqrt()*r);
    vec![x*scale, y*scale, z*scale].into_boxed_slice()
}
