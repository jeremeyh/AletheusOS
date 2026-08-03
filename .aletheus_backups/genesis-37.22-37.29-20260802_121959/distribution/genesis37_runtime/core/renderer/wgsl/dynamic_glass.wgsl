struct Glass { ior:f32, dispersion:f32, opacity:f32, phase:f32 }
@group(0) @binding(0) var<uniform> glass:Glass;
struct In { @location(0) normal:vec3<f32>, @location(1) view:vec3<f32>, @location(2) base:vec3<f32> }
@fragment fn main(i:In)->@location(0) vec4<f32>{
  let n=normalize(i.normal); let v=normalize(i.view);
  let f0=pow((glass.ior-1.0)/(glass.ior+1.0),2.0);
  let fresnel=f0+(1.0-f0)*pow(1.0-max(dot(n,v),0.0),5.0);
  let chroma=vec3<f32>(glass.dispersion,0.0,-glass.dispersion);
  let color=i.base+chroma*fresnel+vec3<f32>(fresnel);
  return vec4<f32>(color,mix(glass.opacity,0.98,glass.phase));
}
