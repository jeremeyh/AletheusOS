use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub struct RemKernel {
    seed: u32,
    target_frame_ms: f32,
}

#[wasm_bindgen]
impl RemKernel {
    #[wasm_bindgen(constructor)]
    pub fn new(seed: u32, target_hz: f32) -> Self {
        let safe_hz = target_hz.max(1.0);
        Self {
            seed,
            target_frame_ms: 1000.0 / safe_hz,
        }
    }

    #[wasm_bindgen]
    pub fn seed(&self) -> u32 {
        self.seed
    }

    #[wasm_bindgen]
    pub fn meantime_quotient(
        &self,
        mean_frame_ms: f32,
        standard_deviation_ms: f32,
        dropped_ratio: f32,
    ) -> f32 {
        let budget = (self.target_frame_ms / mean_frame_ms.max(0.001))
            .clamp(0.0, 1.0);
        let jitter = (
            1.0 - standard_deviation_ms / self.target_frame_ms
        ).clamp(0.0, 1.0);
        let delivery = (1.0 - dropped_ratio).clamp(0.0, 1.0);

        budget * 0.48 + jitter * 0.34 + delivery * 0.18
    }
}
