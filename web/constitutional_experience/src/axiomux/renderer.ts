import { GPUScheduler } from "./gpuScheduler.js";
import { SceneGraph } from "./sceneGraph.js";

export class AxiomUXRenderer {
  readonly scene = new SceneGraph();
  readonly scheduler = new GPUScheduler();
  private device?: GPUDevice;
  private context?: GPUCanvasContext;

  async initialize(canvas: HTMLCanvasElement): Promise<void> {
    if (!navigator.gpu) throw new Error("WebGPU unavailable");
    const adapter = await navigator.gpu.requestAdapter({ powerPreference: "high-performance" });
    if (!adapter) throw new Error("WebGPU adapter unavailable");
    this.device = await adapter.requestDevice();
    this.context = canvas.getContext("webgpu") ?? undefined;
    if (!this.context) throw new Error("WebGPU canvas context unavailable");
    this.context.configure({
      device: this.device,
      format: navigator.gpu.getPreferredCanvasFormat(),
      alphaMode: "premultiplied",
    });
  }

  async renderFrame(): Promise<void> {
    if (!this.device || !this.context) throw new Error("renderer not initialized");
    await this.scheduler.drain();
    const encoder = this.device.createCommandEncoder();
    const view = this.context.getCurrentTexture().createView();
    const pass = encoder.beginRenderPass({
      colorAttachments: [{
        view,
        clearValue: { r: 0.01, g: 0.02, b: 0.05, a: 1 },
        loadOp: "clear",
        storeOp: "store",
      }],
    });
    pass.end();
    this.device.queue.submit([encoder.finish()]);
  }
}
