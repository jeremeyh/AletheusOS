struct Particle {
  position: vec2<f32>,
  velocity: vec2<f32>,
  target: vec2<f32>,
  phase: f32,
  mass: f32,
  charge: f32,
  seed: f32,
  size: f32,
};

struct SimulationParams {
  cursor_pos: vec2<f32>,
  delta_time: f32,
  time: f32,
  magnetic_strength: f32,
  particle_count: u32,
  stiffness: f32,
  damping: f32,
  width: f32,
  height: f32,
};

@group(0) @binding(0)
var<storage, read_write> particles: array<Particle>;

@group(0) @binding(1)
var<uniform> params: SimulationParams;

fn hash21(value: vec2<f32>) -> f32 {
  return fract(sin(dot(value, vec2<f32>(127.1, 311.7))) * 43758.5453123);
}

fn noise_field(position: vec2<f32>, time: f32, seed: f32) -> vec2<f32> {
  let a = hash21(position * 0.011 + vec2<f32>(time, seed));
  let b = hash21(position.yx * 0.013 + vec2<f32>(seed, -time));
  return (vec2<f32>(a, b) * 2.0 - 1.0) * 25.0;
}

@compute @workgroup_size(64)
fn main(@builtin(global_invocation_id) id: vec3<u32>) {
  let index = id.x;
  if (index >= params.particle_count) {
    return;
  }

  var particle = particles[index];
  let phase = clamp(particle.phase, 0.0, 1.0);
  let spring_force =
    (particle.target - particle.position) * params.stiffness * phase;
  let damping_force = -params.damping * particle.velocity;
  let ambient_force =
    noise_field(particle.position, params.time, particle.seed) *
    (1.0 - phase);

  let pointer_delta = params.cursor_pos - particle.position;
  let distance = max(length(pointer_delta), 10.0);
  let direction = pointer_delta / distance;
  let magnetic =
    direction *
    (params.magnetic_strength * particle.charge /
      (distance * distance + 100.0));

  let acceleration =
    (spring_force + damping_force + ambient_force + magnetic) /
    max(particle.mass, 0.001);

  particle.velocity += acceleration * params.delta_time;
  particle.position += particle.velocity * params.delta_time;

  particle.position.x =
    (particle.position.x + params.width) % params.width;
  particle.position.y =
    (particle.position.y + params.height) % params.height;

  particles[index] = particle;
}
