type WasmModule = Record<string, unknown>;

export interface WasmRuntimeState {
  livingPhysics?: WasmModule;
  resonanceField?: WasmModule;
  ambientElasticity?: WasmModule;
  available: boolean;
  errors: string[];
}

const modules = {
  livingPhysics: "/wasm/living_physics_core/living_physics_core.js",
  resonanceField: "/wasm/resonance_field_core/resonance_field_core.js",
  ambientElasticity: "/wasm/ambient_elasticity_core/ambient_elasticity_core.js",
} as const;

async function loadModule(path: string): Promise<WasmModule> {
  const imported = (await import(/* @vite-ignore */ path)) as WasmModule & { default?: () => Promise<unknown> };
  if (typeof imported.default === "function") await imported.default();
  return imported;
}

export async function initializeWasmRuntime(): Promise<WasmRuntimeState> {
  const state: WasmRuntimeState = { available: false, errors: [] };
  for (const [key, path] of Object.entries(modules)) {
    try {
      state[key as keyof typeof modules] = await loadModule(path);
    } catch (error) {
      state.errors.push(`${key}: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
  state.available = Boolean(state.livingPhysics && state.resonanceField && state.ambientElasticity);
  return state;
}
