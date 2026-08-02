use serde::{Deserialize,Serialize};
#[derive(Debug,Clone,Serialize,Deserialize)]
pub struct Match { pub participants: Vec<String>, pub cash_adjustments: Vec<f64> }
pub fn zero_sum(values:[f64;3])->[f64;3] { [values[2]-values[0], values[0]-values[1], values[1]-values[2]] }
