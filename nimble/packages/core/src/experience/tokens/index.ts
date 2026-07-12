import { instrumentationTokens } from "./instrumentation";
import { primitiveTokens } from "./primitives";
import { TokenRegistry } from "./registry";
import { semanticTokens } from "./semantic";
import { validateTokens } from "./validator";

export * from "./instrumentation";
export * from "./primitives";
export * from "./registry";
export * from "./semantic";
export * from "./types";
export * from "./validator";

export function createExperienceTokenRegistry(): TokenRegistry {
  const registry = new TokenRegistry();

  registry.register(
    "primitive",
    primitiveTokens,
  );

  registry.register(
    "semantic",
    semanticTokens,
  );

  registry.register(
    "instrumentation",
    instrumentationTokens,
  );

  const validation = validateTokens(
    registry.entries(),
  );

  if (!validation.valid) {
    throw new Error(
      [
        "Experience token validation failed:",
        ...validation.failures,
      ].join("\n"),
    );
  }

  return registry;
}

export const experienceTokens =
  createExperienceTokenRegistry().snapshot();
