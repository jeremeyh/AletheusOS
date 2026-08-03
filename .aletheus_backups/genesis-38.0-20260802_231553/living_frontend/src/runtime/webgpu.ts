export interface RendererStatus {
  mode: "webgpu" | "canvas2d";
  adapterName: string;
}

const shader = `
struct Uniforms { time: f32, phase: f32, width: f32, height: f32 };
@group(0) @binding(0) var<uniform> u: Uniforms;

@vertex fn vs(@builtin(vertex_index) i: u32) -> @builtin(position) vec4<f32> {
  var p = array<vec2<f32>, 3>(vec2(-1.0,-1.0), vec2(3.0,-1.0), vec2(-1.0,3.0));
  return vec4(p[i],0.0,1.0);
}

fn hash(p: vec2<f32>) -> f32 { return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }

@fragment fn fs(@builtin(position) p: vec4<f32>) -> @location(0) vec4<f32> {
  let uv = p.xy / vec2(u.width,u.height);
  let centered = uv - vec2(0.5);
  let r = length(centered);
  let breath = 0.5 + 0.5*sin(u.time*0.94);
  let wave = sin((r*18.0-u.time*1.6)+hash(floor(uv*42.0))*0.8);
  let nebula = vec3(0.08,0.18,0.38) + vec3(0.28,0.07,0.48)*wave*0.32;
  let crystal = vec3(0.04,0.42,0.54) + vec3(0.68,0.78,0.94)*pow(max(0.0,1.0-r),3.0);
  let col = mix(nebula,crystal,u.phase) + breath*0.025;
  let vignette = smoothstep(0.92,0.18,r);
  return vec4(col*vignette,1.0);
}`;

export async function startRenderer(canvas: HTMLCanvasElement, phaseProvider: () => number): Promise<RendererStatus> {
  const nav = navigator as Navigator & { gpu?: any };
  if (!nav.gpu) return startCanvasFallback(canvas, phaseProvider);
  const adapter = await nav.gpu.requestAdapter({ powerPreference: "high-performance" });
  if (!adapter) return startCanvasFallback(canvas, phaseProvider);
  const device = await adapter.requestDevice();
  const context = canvas.getContext("webgpu") as any;
  if (!context) return startCanvasFallback(canvas, phaseProvider);
  const format = nav.gpu.getPreferredCanvasFormat();
  context.configure({ device, format, alphaMode: "opaque" });
  const module = device.createShaderModule({ code: shader });
  const pipeline = device.createRenderPipeline({
    layout: "auto",
    vertex: { module, entryPoint: "vs" },
    fragment: { module, entryPoint: "fs", targets: [{ format }] },
    primitive: { topology: "triangle-list" },
  });
  const buffer = device.createBuffer({ size: 16, usage: 0x40 | 0x08 });
  const bindGroup = device.createBindGroup({ layout: pipeline.getBindGroupLayout(0), entries: [{ binding: 0, resource: { buffer } }] });
  const resize = () => {
    const ratio = Math.min(devicePixelRatio, 2);
    canvas.width = Math.max(1, Math.floor(canvas.clientWidth * ratio));
    canvas.height = Math.max(1, Math.floor(canvas.clientHeight * ratio));
  };
  const frame = (time: number) => {
    resize();
    device.queue.writeBuffer(buffer, 0, new Float32Array([time / 1000, phaseProvider(), canvas.width, canvas.height]));
    const encoder = device.createCommandEncoder();
    const pass = encoder.beginRenderPass({ colorAttachments: [{ view: context.getCurrentTexture().createView(), loadOp: "clear", storeOp: "store", clearValue: { r: 0.01, g: 0.015, b: 0.03, a: 1 } }] });
    pass.setPipeline(pipeline); pass.setBindGroup(0, bindGroup); pass.draw(3); pass.end();
    device.queue.submit([encoder.finish()]); requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
  return { mode: "webgpu", adapterName: adapter.info?.description || "WebGPU adapter" };
}

function startCanvasFallback(canvas: HTMLCanvasElement, phaseProvider: () => number): RendererStatus {
  const ctx = canvas.getContext("2d");
  const frame = (time: number) => {
    if (!ctx) return;
    const ratio = Math.min(devicePixelRatio, 2);
    canvas.width = Math.max(1, Math.floor(canvas.clientWidth * ratio)); canvas.height = Math.max(1, Math.floor(canvas.clientHeight * ratio));
    const phase = phaseProvider();
    const g = ctx.createRadialGradient(canvas.width*.5,canvas.height*.42,10,canvas.width*.5,canvas.height*.5,canvas.width*.7);
    g.addColorStop(0,`rgba(${Math.round(20+phase*80)},${Math.round(80+phase*90)},${Math.round(140+phase*90)},1)`);
    g.addColorStop(1,"#05070d"); ctx.fillStyle=g; ctx.fillRect(0,0,canvas.width,canvas.height);
    ctx.globalAlpha=.12; ctx.strokeStyle="#9eefff"; ctx.lineWidth=1;
    for(let i=0;i<10;i++){const r=(i*90+(time*.02)%90);ctx.beginPath();ctx.arc(canvas.width*.5,canvas.height*.5,r,0,Math.PI*2);ctx.stroke();}
    ctx.globalAlpha=1; requestAnimationFrame(frame);
  };
  requestAnimationFrame(frame);
  return { mode: "canvas2d", adapterName: "Canvas 2D fallback" };
}
