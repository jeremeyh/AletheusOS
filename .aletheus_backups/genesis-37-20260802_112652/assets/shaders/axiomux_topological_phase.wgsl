struct Uniforms { mvp: mat4x4<f32>, time: f32, phase: f32, motion_scale: f32 }
@group(0) @binding(0) var<uniform> u: Uniforms;
struct In { @location(0) p: vec3<f32>, @location(1) n: vec3<f32> }
struct Out { @builtin(position) p: vec4<f32>, @location(0) n: vec3<f32>, @location(1) local: vec3<f32> }
@vertex fn main_vs(i: In) -> Out { var o:Out; let d=(1.0-clamp(u.phase,0.0,1.0))*0.35*sin(i.p.x*3.0+u.time)*u.motion_scale; let p=i.p+i.n*d; o.p=u.mvp*vec4<f32>(p,1.0); o.n=i.n; o.local=p; return o; }
@fragment fn main_fs(i:Out)->@location(0) vec4<f32>{ let f=pow(1.0-max(dot(normalize(-i.local),normalize(i.n)),0.0),3.5); let n=vec3<f32>(0.42,0.12,0.95); let c=vec3<f32>(0.9,0.95,1.0)*f*2.0+vec3<f32>(0.1); let p=clamp(u.phase,0.0,1.0); return vec4<f32>(mix(n,c,p),mix(0.4,0.95,p)); }
