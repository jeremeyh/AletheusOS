use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;

#[derive(Clone, Copy, Debug, Deserialize, Serialize)]
pub struct EvidenceNode {
    provenance: f64,
    consensus: f64,
    utility: f64,
    veracity: f64,
    contradiction: f64,
    temporal_delta: f64,
}

#[derive(Clone, Copy, Debug, Deserialize, Serialize)]
pub struct PhysicsState {
    mass: f64,
    consensus_pressure: f64,
    shear: f64,
    temporal_momentum: f64,
    phase: u8,
}

fn clamp01(v: f64) -> f64 { v.clamp(0.0, 1.0) }

#[wasm_bindgen]
pub fn evaluate_node(node: JsValue, age_seconds: f64) -> Result<JsValue, JsValue> {
    let node: EvidenceNode = serde_wasm_bindgen::from_value(node)?;
    let mass = node.utility.max(0.0) * clamp01(node.provenance) * clamp01(node.consensus);
    let shear = clamp01(node.contradiction) * (1.0 + node.temporal_delta.abs().min(1.0));
    let temporal_momentum = node.temporal_delta * (-age_seconds.max(0.0) / 86_400.0).exp();
    let phase = if node.veracity < 0.60 { 0 } else if node.veracity < 0.85 { 1 } else if node.veracity < 0.98 { 2 } else { 3 };
    let state = PhysicsState {
        mass,
        consensus_pressure: clamp01(node.consensus),
        shear,
        temporal_momentum,
        phase,
    };
    serde_wasm_bindgen::to_value(&state).map_err(Into::into)
}

#[wasm_bindgen]
pub struct SpringBatch {
    positions: Vec<f32>,
    targets: Vec<f32>,
    velocities: Vec<f32>,
    stiffness: f32,
    damping_ratio: f32,
    mass: f32,
}

#[wasm_bindgen]
impl SpringBatch {
    #[wasm_bindgen(constructor)]
    pub fn new(node_count: usize, stiffness: f32, damping_ratio: f32, mass: f32) -> Self {
        let width = node_count.saturating_mul(3);
        Self {
            positions: vec![0.0; width],
            targets: vec![0.0; width],
            velocities: vec![0.0; width],
            stiffness: stiffness.max(0.0),
            damping_ratio: damping_ratio.max(0.0),
            mass: mass.max(0.0001),
        }
    }

    pub fn set_target(&mut self, index: usize, x: f32, y: f32, z: f32) {
        let base = index.saturating_mul(3);
        if base + 2 < self.targets.len() {
            self.targets[base] = x; self.targets[base + 1] = y; self.targets[base + 2] = z;
        }
    }

    pub fn update(&mut self, dt: f32) {
        let steps = 4;
        let h = dt.clamp(0.0, 0.032) / steps as f32;
        let c = 2.0 * self.damping_ratio * (self.stiffness * self.mass).sqrt();
        for _ in 0..steps {
            for i in 0..self.positions.len() {
                let force = -self.stiffness * (self.positions[i] - self.targets[i]);
                let damping = -c * self.velocities[i];
                let acceleration = (force + damping) / self.mass;
                self.velocities[i] += acceleration * h;
                self.positions[i] += self.velocities[i] * h;
            }
        }
    }

    pub fn positions_ptr(&self) -> *const f32 { self.positions.as_ptr() }
    pub fn positions_len(&self) -> usize { self.positions.len() }
}
