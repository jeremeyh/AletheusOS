\
export interface LIGHTSTelemetry {
  veracity: number;
  consensus: number;
  contradiction: number;
  elasticity: number;
  fieldDensity: number;
  resonance: number;
  founderMode: number;
  curvature?: number;
  phaseOrder?: number;
  entropyHamiltonian?: number;
  attraction?: number;
  shear?: number;
}

const VERTEX_SHADER = `#version 300 es
in vec2 a_position;
out vec2 v_uv;

void main() {
  v_uv = a_position * 0.5 + 0.5;
  gl_Position = vec4(a_position, 0.0, 1.0);
}`;

const FRAGMENT_SHADER = `#version 300 es
precision highp float;

in vec2 v_uv;
out vec4 fragColor;

uniform vec2 u_resolution;
uniform float u_time;
uniform float u_veracity;
uniform float u_consensus;
uniform float u_contradiction;
uniform float u_elasticity;
uniform float u_density;
uniform float u_resonance;
uniform float u_founder_mode;
uniform float u_curvature;
uniform float u_phase_order;
uniform float u_entropy_hamiltonian;
uniform float u_attraction;
uniform float u_shear;

#define PI 3.14159265359
#define TAU 6.28318530718

float hash21(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

float valueNoise(vec2 p) {
  vec2 i = floor(p);
  vec2 f = fract(p);
  f = f * f * (3.0 - 2.0 * f);
  return mix(
    mix(hash21(i), hash21(i + vec2(1.0, 0.0)), f.x),
    mix(hash21(i + vec2(0.0, 1.0)), hash21(i + vec2(1.0, 1.0)), f.x),
    f.y
  );
}

float fbm(vec2 p) {
  float value = 0.0;
  float amplitude = 0.5;
  mat2 rotation = mat2(0.80, -0.60, 0.60, 0.80);

  for (int octave = 0; octave < 5; octave++) {
    value += amplitude * valueNoise(p);
    p = rotation * p * 2.03 + 17.0;
    amplitude *= 0.5;
  }
  return value;
}

vec2 fluidVelocity(vec2 p, float t) {
  float u = sin(p.y * 4.0 + t * 0.8)
    + cos(p.x * 2.5 - t * 0.5);
  float v = cos(p.x * 4.0 - t * 0.8)
    + sin(p.y * 2.5 + t * 0.5);

  float turbulence = u_contradiction * 8.0 + u_shear * 4.0;
  u += sin(p.y * 20.0 + t * 3.0) * 0.05 * turbulence;
  v += cos(p.x * 20.0 + t * 3.0) * 0.05 * turbulence;

  return vec2(u, v) * (
    0.025
    + u_elasticity * 0.075
    + u_curvature * 0.025
  );
}

vec3 liquidMetalReflection(
  vec2 p,
  vec2 velocity,
  float density
) {
  float micro = fbm(p * 5.0 + velocity * 1.5 + u_time * 0.025);
  vec3 normal = normalize(vec3(
    velocity.x * 2.0 + (micro - 0.5) * 0.35,
    velocity.y * 2.0 + (micro - 0.5) * 0.35,
    1.0 - density * 0.45
  ));

  vec3 lightDir = normalize(vec3(
    sin(u_time * 0.20),
    cos(u_time * 0.20),
    0.82
  ));
  vec3 viewDir = vec3(0.0, 0.0, 1.0);
  vec3 halfVector = normalize(lightDir + viewDir);

  float specularPower = 30.0
    + (1.0 - u_elasticity) * 70.0
    + u_phase_order * 24.0;
  float spec = pow(
    max(dot(normal, halfVector), 0.0),
    specularPower
  );
  float fresnel = pow(
    1.0 - max(dot(normal, viewDir), 0.0),
    3.0
  );

  vec3 voidBase = vec3(0.008, 0.014, 0.026);
  vec3 polarizedBlue = vec3(0.05, 0.13, 0.28);
  vec3 goldBase = vec3(0.84, 0.63, 0.19);
  vec3 metallicGlint = vec3(1.0, 0.94, 0.68)
    * spec * (1.2 + u_veracity * 0.9);

  vec3 ambient = mix(
    voidBase,
    polarizedBlue,
    fresnel * (0.24 + u_curvature * 0.34)
  );
  ambient += goldBase * micro * 0.10 * u_attraction;

  return ambient + metallicGlint;
}

void main() {
  vec2 st = (
    gl_FragCoord.xy - 0.5 * u_resolution.xy
  ) / u_resolution.y;

  float breath = sin(u_time * (TAU / 10.0));
  st *= 1.0 - breath * 0.003 * u_elasticity;

  float lensRadius = length(st);
  st *= 1.0
    + u_contradiction * 0.018 * smoothstep(0.62, 0.0, lensRadius)
    - u_resonance * 0.009 * smoothstep(0.72, 0.0, lensRadius);

  vec2 velocity = fluidVelocity(st, u_time);
  vec2 advected = st - velocity * (
    0.14 + 0.10 * u_elasticity
  );

  vec3 surface = liquidMetalReflection(
    advected,
    velocity,
    u_density
  );

  float current = fbm(
    advected * (2.5 + u_density * 3.0)
    + vec2(u_time * 0.018, -u_time * 0.013)
  );
  vec3 constitutionalGold = vec3(0.92, 0.70, 0.22);
  vec3 contradictionCrimson = vec3(0.76, 0.08, 0.12);
  vec3 resonanceBlue = vec3(0.10, 0.34, 0.72);

  surface += constitutionalGold
    * smoothstep(0.66, 0.96, current)
    * 0.055
    * u_attraction;

  surface += contradictionCrimson
    * u_contradiction
    * u_entropy_hamiltonian
    * 0.24;

  surface += resonanceBlue
    * u_resonance
    * u_curvature
    * 0.08;

  if (u_founder_mode > 0.01) {
    float gridX = step(
      0.982,
      fract((st.x + velocity.x) * 30.0)
    );
    float gridY = step(
      0.982,
      fract((st.y + velocity.y) * 30.0)
    );
    surface += vec3(0.0, 0.55, 0.90)
      * (gridX + gridY)
      * 0.12
      * u_founder_mode;
  }

  fragColor = vec4(surface, 1.0);
}`;

export class LIGHTSEngine {
  private readonly gl: WebGL2RenderingContext;
  private readonly program: WebGLProgram;
  private readonly uniforms: Record<
    string,
    WebGLUniformLocation | null
  >;
  private animationFrame = 0;
  private readonly startedAt = performance.now();

  private telemetry: LIGHTSTelemetry = {
    veracity: 0.982,
    consensus: 0.947,
    contradiction: 0.061,
    elasticity: 0.54,
    fieldDensity: 0.72,
    resonance: 0.965,
    founderMode: 0,
    curvature: 0.76,
    phaseOrder: 0.82,
    entropyHamiltonian: 0.17,
    attraction: 0.88,
    shear: 0.08,
  };

  constructor(private readonly canvas: HTMLCanvasElement) {
    const gl = canvas.getContext("webgl2", {
      alpha: false,
      antialias: true,
      depth: false,
      stencil: false,
      powerPreference: "high-performance",
    });

    if (!gl) {
      throw new Error(
        "LIGHTS™ requires WebGL2 hardware acceleration.",
      );
    }
    this.gl = gl;

    const compile = (
      source: string,
      type: number,
    ): WebGLShader => {
      const shader = gl.createShader(type);
      if (!shader) {
        throw new Error("Unable to allocate LIGHTS shader.");
      }
      gl.shaderSource(shader, source);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(
        shader,
        gl.COMPILE_STATUS,
      )) {
        throw new Error(
          gl.getShaderInfoLog(shader)
            ?? "LIGHTS shader compilation failed.",
        );
      }
      return shader;
    };

    const program = gl.createProgram();
    if (!program) {
      throw new Error("Unable to allocate LIGHTS program.");
    }
    gl.attachShader(
      program,
      compile(VERTEX_SHADER, gl.VERTEX_SHADER),
    );
    gl.attachShader(
      program,
      compile(FRAGMENT_SHADER, gl.FRAGMENT_SHADER),
    );
    gl.linkProgram(program);
    if (!gl.getProgramParameter(
      program,
      gl.LINK_STATUS,
    )) {
      throw new Error(
        gl.getProgramInfoLog(program)
          ?? "LIGHTS program link failed.",
      );
    }
    gl.useProgram(program);
    this.program = program;

    const positions = new Float32Array([
      -1, -1, 1, -1, -1, 1,
      -1, 1, 1, -1, 1, 1,
    ]);
    const buffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      positions,
      gl.STATIC_DRAW,
    );

    const attribute = gl.getAttribLocation(
      program,
      "a_position",
    );
    gl.enableVertexAttribArray(attribute);
    gl.vertexAttribPointer(
      attribute,
      2,
      gl.FLOAT,
      false,
      0,
      0,
    );

    const location = (name: string) =>
      gl.getUniformLocation(program, name);

    this.uniforms = {
      resolution: location("u_resolution"),
      time: location("u_time"),
      veracity: location("u_veracity"),
      consensus: location("u_consensus"),
      contradiction: location("u_contradiction"),
      elasticity: location("u_elasticity"),
      density: location("u_density"),
      resonance: location("u_resonance"),
      founderMode: location("u_founder_mode"),
      curvature: location("u_curvature"),
      phaseOrder: location("u_phase_order"),
      entropyHamiltonian: location(
        "u_entropy_hamiltonian",
      ),
      attraction: location("u_attraction"),
      shear: location("u_shear"),
    };

    this.resize();
  }

  updateTelemetry(
    next: Partial<LIGHTSTelemetry>,
  ): void {
    this.telemetry = {
      ...this.telemetry,
      ...next,
    };
  }

  resize(): void {
    const dpr = Math.min(
      window.devicePixelRatio || 1,
      2,
    );
    this.canvas.width = Math.floor(
      this.canvas.clientWidth * dpr,
    );
    this.canvas.height = Math.floor(
      this.canvas.clientHeight * dpr,
    );
    this.gl.viewport(
      0,
      0,
      this.canvas.width,
      this.canvas.height,
    );
  }

  start(): void {
    const draw = (timestamp: number) => {
      const gl = this.gl;
      const time = (
        timestamp - this.startedAt
      ) * 0.001;
      const telemetry = this.telemetry;

      gl.useProgram(this.program);
      gl.uniform2f(
        this.uniforms.resolution,
        this.canvas.width,
        this.canvas.height,
      );
      gl.uniform1f(this.uniforms.time, time);
      gl.uniform1f(
        this.uniforms.veracity,
        telemetry.veracity,
      );
      gl.uniform1f(
        this.uniforms.consensus,
        telemetry.consensus,
      );
      gl.uniform1f(
        this.uniforms.contradiction,
        telemetry.contradiction,
      );
      gl.uniform1f(
        this.uniforms.elasticity,
        telemetry.elasticity,
      );
      gl.uniform1f(
        this.uniforms.density,
        telemetry.fieldDensity,
      );
      gl.uniform1f(
        this.uniforms.resonance,
        telemetry.resonance,
      );
      gl.uniform1f(
        this.uniforms.founderMode,
        telemetry.founderMode,
      );
      gl.uniform1f(
        this.uniforms.curvature,
        telemetry.curvature ?? 0,
      );
      gl.uniform1f(
        this.uniforms.phaseOrder,
        telemetry.phaseOrder ?? 0,
      );
      gl.uniform1f(
        this.uniforms.entropyHamiltonian,
        telemetry.entropyHamiltonian ?? 0,
      );
      gl.uniform1f(
        this.uniforms.attraction,
        telemetry.attraction ?? 0,
      );
      gl.uniform1f(
        this.uniforms.shear,
        telemetry.shear ?? 0,
      );

      gl.drawArrays(gl.TRIANGLES, 0, 6);
      this.animationFrame = requestAnimationFrame(draw);
    };

    this.animationFrame = requestAnimationFrame(draw);
  }

  stop(): void {
    cancelAnimationFrame(this.animationFrame);
  }
}
