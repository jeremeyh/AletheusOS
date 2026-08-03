struct Params { time:f32, phase:f32, tension:f32, motion_scale:f32 }
@group(0) @binding(0) var<uniform> p:Params;
struct Vin { @location(0) pos:vec3<f32>, @location(1) normal:vec3<f32> }
struct Vout { @builtin(position) pos:vec4<f32>, @location(0) normal:vec3<f32> }
fn field(v:vec3<f32>)->f32{ return sin(v.x*3.1+p.time)*cos(v.y*2.7-p.time)*sin(v.z*4.3); }
@vertex fn main(i:Vin)->Vout{
  var o:Vout;
  let fluid=(1.0-clamp(p.phase,0.0,1.0))*field(i.pos)*0.28;
  let shear=p.tension*sin(p.time*18.0+i.pos.y*8.0)*0.04;
  let q=i.pos+i.normal*(fluid+shear)*p.motion_scale;
  o.pos=vec4<f32>(q,1.0); o.normal=i.normal; return o;
}
