use serde::Serialize;
use wasm_bindgen::prelude::*;

#[derive(Serialize)]
struct TelemetrySummary {
    average_frame_ms: f64,
    p95_frame_ms: f64,
    dropped_frame_ratio: f64,
    meantime_quotient: f64,
}

#[wasm_bindgen]
pub fn summarize_frame_times(values: Box<[f64]>, target_frame_ms: f64) -> Result<JsValue, JsValue> {
    if values.is_empty() { return Err(JsValue::from_str("frame times required")); }
    let mut sorted = values.into_vec();
    sorted.sort_by(|a,b| a.total_cmp(b));
    let sum: f64 = sorted.iter().sum();
    let average = sum / sorted.len() as f64;
    let p95_index = ((sorted.len() as f64 * 0.95).ceil() as usize).saturating_sub(1);
    let p95 = sorted[p95_index.min(sorted.len()-1)];
    let dropped = sorted.iter().filter(|v| **v > target_frame_ms * 1.5).count() as f64 / sorted.len() as f64;
    let meantime_quotient = (target_frame_ms / average.max(target_frame_ms)).clamp(0.0, 1.0);
    serde_wasm_bindgen::to_value(&TelemetrySummary {
        average_frame_ms: average,
        p95_frame_ms: p95,
        dropped_frame_ratio: dropped,
        meantime_quotient,
    }).map_err(Into::into)
}
