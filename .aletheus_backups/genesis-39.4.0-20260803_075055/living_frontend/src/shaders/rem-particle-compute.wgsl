struct Particle {
  position: vec2<f32>,
  velocity: vec2<f32>,
  anchor: vec2<f32>,
  coherence: f32,
  charge: f32,
  seed: f32,
  size: f32,
};

struct RuntimeUniforms {
  delta_seconds: f32,
  time_seconds: f32,
  coherence_target: f32,
  lattice_stiffness: f32,
  damping: f32,
  brownian_strength: f32,
  magnetic_strength: f32,
  magnetic_radius: f32,
  pointer: vec2<f32>,
  pointer_active: f32,
  width: f32,
  height: f32,
};

@group(0) @binding(0)
var<storage, read_write> particles: array<Particle>;

@group(0) @binding(1)
var<uniform> runtime: RuntimeUniforms;

fn hash21(value: vec2<f32>) -> f32 {
  let dot_value = dot(value, vec2<f32>(127.1, 311.7));
  return fract(sin(dot_value) * 43758.5453123);
}

@compute @workgroup_size(256)
fn update_particles(@builtin(global_invocation_id) id: vec3<u32>) {
  let index = id.x;
  if (index >= arrayLength(&particles)) {
    return;
  }

  var particle = particles[index];
  let dt = min(runtime.delta_seconds, 0.05);
  particle.coherence +=
    (runtime.coherence_target - particle.coherence) *
    min(1.0, dt * 4.6);

  let noise_x =
    hash21(particle.position * 0.003 + runtime.time_seconds) * 2.0 - 1.0;
  let noise_y =
    hash21(particle.position.yx * 0.004 - runtime.time_seconds) * 2.0 - 1.0;

  var force = vec2<f32>(noise_x, noise_y) * runtime.brownian_strength;
  force +=
    (particle.anchor - particle.position) *
    runtime.lattice_stiffness *
    particle.coherence *
    0.00008;

  if (runtime.pointer_active > 0.5) {
    let delta = particle.position - runtime.pointer;
    let distance_squared = max(dot(delta, delta), 36.0);
    let radius_squared =
      runtime.magnetic_radius * runtime.magnetic_radius;

    if (distance_squared < radius_squared) {
      let distance = sqrt(distance_squared);
      let attenuation = 1.0 - distance / runtime.magnetic_radius;
      let magnetic =
        runtime.magnetic_strength *
        particle.charge *
        attenuation *
        attenuation /
        distance_squared;
      force += normalize(delta) * magnetic;
    }
  }

  particle.velocity += force;
  particle.velocity *= exp(-runtime.damping * dt * 0.045);
  particle.position += particle.velocity;

  particle.position.x =
    (particle.position.x + runtime.width) % runtime.width;
  particle.position.y =
    (particle.position.y + runtime.height) % runtime.height;

  particles[index] = particle;
}
