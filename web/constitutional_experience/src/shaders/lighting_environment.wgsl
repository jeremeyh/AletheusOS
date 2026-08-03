struct LightState { urgency:f32, uncertainty:f32, compliance:f32, time:f32 }
@group(0) @binding(0) var<uniform> s:LightState;
@fragment fn main()->@location(0) vec4<f32>{
  let pulse=0.5+0.5*sin(s.time*0.9424778);
  let cool=vec3<f32>(0.04,0.18,0.35);
  let urgent=vec3<f32>(0.8,0.18,0.08);
  let governed=vec3<f32>(0.08,0.72,0.55);
  let color=mix(mix(cool,urgent,s.urgency),governed,s.compliance*0.35);
  return vec4<f32>(color*(0.9+0.1*pulse*s.uncertainty),1.0);
}
