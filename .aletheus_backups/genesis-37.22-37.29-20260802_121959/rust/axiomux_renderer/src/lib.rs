use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;

#[derive(Deserialize)]
struct SceneNode {
    id: String,
    mass: f32,
    veracity: f32,
    tension: f32,
}

#[derive(Serialize)]
struct RenderCommand {
    id: String,
    scale: f32,
    phase: u8,
    emissive: f32,
    distortion: f32,
}

#[wasm_bindgen]
pub fn compile_scene(nodes: JsValue) -> Result<JsValue, JsValue> {
    let nodes: Vec<SceneNode> = serde_wasm_bindgen::from_value(nodes)?;
    let commands: Vec<RenderCommand> = nodes.into_iter().map(|node| {
        let phase = if node.veracity < 0.60 {0} else if node.veracity < 0.85 {1} else if node.veracity < 0.98 {2} else {3};
        RenderCommand {
            id: node.id,
            scale: 0.75 + node.mass.max(0.0).sqrt().min(3.0),
            phase,
            emissive: (0.15 + node.mass * 0.25).clamp(0.0, 2.0),
            distortion: node.tension.clamp(0.0, 1.0),
        }
    }).collect();
    serde_wasm_bindgen::to_value(&commands).map_err(Into::into)
}
