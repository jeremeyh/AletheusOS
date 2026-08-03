struct SurfaceUniforms {
  resolution: vec2<f32>,
  time: f32,
  coherence: f32,
  thermal_pressure: f32,
  blend_softness: f32,
};

@group(0) @binding(0)
var<uniform> surface: SurfaceUniforms;

fn rounded_box(point: vec2<f32>, half_size: vec2<f32>, radius: f32) -> f32 {
  let q = abs(point) - half_size + vec2<f32>(radius);
  return min(max(q.x, q.y), 0.0) + length(max(q, vec2<f32>(0.0))) - radius;
}

fn smooth_union(distance_a: f32, distance_b: f32, softness: f32) -> f32 {
  let h = clamp(0.5 + 0.5 * (distance_b - distance_a) / softness, 0.0, 1.0);
  return mix(distance_b, distance_a, h) - softness * h * (1.0 - h);
}

fn fresnel(view_dot_normal: f32, power: f32) -> f32 {
  return pow(1.0 - clamp(view_dot_normal, 0.0, 1.0), power);
}

@fragment
fn main(@builtin(position) position: vec4<f32>) -> @location(0) vec4<f32> {
  let uv = (position.xy / surface.resolution) * 2.0 - 1.0;
  let aspect = surface.resolution.x / surface.resolution.y;
  let point = vec2<f32>(uv.x * aspect, uv.y);

  let first = rounded_box(point + vec2<f32>(0.28, 0.0), vec2<f32>(0.42, 0.24), 0.11);
  let second = rounded_box(point - vec2<f32>(0.28, 0.0), vec2<f32>(0.42, 0.24), 0.11);
  let distance = smooth_union(first, second, max(0.02, surface.blend_softness));

  let edge = smoothstep(0.02, -0.01, distance);
  let glow = exp(-abs(distance) * 32.0);
  let shimmer = 0.5 + 0.5 * sin(surface.time * 0.7 + point.x * 7.0 + point.y * 4.0);
  let thermal = clamp(surface.thermal_pressure, 0.0, 1.0);

  let obsidian = vec3<f32>(0.025, 0.032, 0.045);
  let titanium = vec3<f32>(0.36, 0.42, 0.5);
  let amber = vec3<f32>(0.91, 0.72, 0.28);
  let cyan = vec3<f32>(0.22, 0.76, 0.96);

  let metal = mix(obsidian, titanium, 0.34 + shimmer * 0.18);
  let emission = mix(cyan, amber, surface.coherence) * glow * (0.18 + thermal * 0.42);
  let color = metal * edge + emission;

  return vec4<f32>(color, edge);
}
