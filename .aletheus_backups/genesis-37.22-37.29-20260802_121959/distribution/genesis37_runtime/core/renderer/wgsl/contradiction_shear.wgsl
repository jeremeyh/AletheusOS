struct Shear { strength:f32, frequency:f32, time:f32, pad:f32 }
@group(0) @binding(0) var<uniform> s:Shear;
@fragment fn main(@builtin(position) p:vec4<f32>)->@location(0) vec4<f32>{
  let bands=abs(sin(p.x*0.04+p.y*0.02+s.time*s.frequency));
  let energy=s.strength*smoothstep(0.75,1.0,bands);
  return vec4<f32>(energy,0.15*energy,0.55*energy,energy);
}
