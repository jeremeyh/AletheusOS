import type { TokenMap } from "./types";

export const instrumentationTokens = {
  "instrumentation.surface":
    "{surface.secondary}",
  "instrumentation.border":
    "{border.subtle}",
  "instrumentation.value":
    "{text.primary}",
  "instrumentation.label":
    "{text.secondary}",

  "instrumentation.status.healthy":
    "{status.healthy}",
  "instrumentation.status.attention":
    "{status.attention}",
  "instrumentation.status.critical":
    "{status.critical}",

  "instrumentation.engine.evidence":
    "{color.cyan.400}",
  "instrumentation.engine.knowledge":
    "{color.blue.400}",
  "instrumentation.engine.reason":
    "{color.violet.400}",
  "instrumentation.engine.memory":
    "{color.gold.300}",
  "instrumentation.engine.bias":
    "{color.amber.400}",
  "instrumentation.engine.risk":
    "{color.red.400}",
  "instrumentation.engine.predictive":
    "{color.green.400}",

  "instrumentation.aletheus-index.primary":
    "{color.gold.400}",
  "instrumentation.aletheus-index.surface":
    "{surface.primary}",

  "instrumentation.thorx.authorized":
    "{color.green.400}",
  "instrumentation.thorx.rejected":
    "{color.red.400}",
  "instrumentation.thorx.guard":
    "{color.gold.500}",
} as const satisfies TokenMap;
