use wasm_bindgen::prelude::*;

#[repr(C)]
pub struct KernelTelemetryPacket {
    pub frame_index: u32,
    pub timestamp_ns: u64,
    pub execution_delta_us: u32,
    pub meantime_quotient: f32,
    pub active_particle_count: u32,
    pub phase_state: u32,
}

#[wasm_bindgen]
pub struct MorphogenesisKernel {
    frame_counter: u32,
    target_frame_time_us: f32,
    history_buffer: Vec<f32>,
    history_index: usize,
    populated_samples: usize,
}

#[wasm_bindgen]
impl MorphogenesisKernel {
    #[wasm_bindgen(constructor)]
    pub fn new(target_fps: f32) -> Self {
        let fps = target_fps.max(1.0);
        Self {
            frame_counter: 0,
            target_frame_time_us: 1_000_000.0 / fps,
            history_buffer: vec![0.0; 128],
            history_index: 0,
            populated_samples: 0,
        }
    }

    pub fn compute_meantime_quotient(&mut self, delta_us: f32) -> f32 {
        self.history_buffer[self.history_index] = delta_us.max(1.0);
        self.history_index = (self.history_index + 1) % self.history_buffer.len();
        self.populated_samples =
            (self.populated_samples + 1).min(self.history_buffer.len());

        let values = &self.history_buffer[..self.populated_samples];
        let mean = values.iter().sum::<f32>() / values.len() as f32;
        let variance = values
            .iter()
            .map(|value| (value - mean).powi(2))
            .sum::<f32>()
            / values.len() as f32;
        let standard_deviation = variance.sqrt();

        let budget = (self.target_frame_time_us / mean).clamp(0.0, 1.0);
        let jitter =
            (1.0 - standard_deviation / self.target_frame_time_us)
                .clamp(0.0, 1.0);

        (budget * 0.62 + jitter * 0.38) * 100.0
    }

    pub fn process_frame_tick(
        &mut self,
        delta_us: f32,
        particle_count: u32,
        phase: u32,
    ) -> Vec<f32> {
        self.frame_counter = self.frame_counter.wrapping_add(1);
        let quotient = self.compute_meantime_quotient(delta_us);

        vec![
            self.frame_counter as f32,
            delta_us,
            quotient,
            particle_count as f32,
            phase as f32,
        ]
    }
}
