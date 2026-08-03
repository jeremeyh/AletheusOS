struct Particle { position: vec4<f32>, velocity: vec4<f32> }
struct Params { dt:f32, attractor_mass:f32, damping:f32, count:u32 }
@group(0) @binding(0) var<storage, read_write> particles: array<Particle>;
@group(0) @binding(1) var<uniform> params: Params;
@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
  let i=gid.x; if(i>=params.count){return;}
  var p=particles[i];
  let r=max(length(p.position.xyz),0.05);
  let gravity=-normalize(p.position.xyz)*(params.attractor_mass/(r*r));
  p.velocity.xyz=(p.velocity.xyz+gravity*params.dt)*params.damping;
  p.position.xyz+=p.velocity.xyz*params.dt;
  particles[i]=p;
}
