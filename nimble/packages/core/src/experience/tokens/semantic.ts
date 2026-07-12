import type { TokenMap } from "./types";

export const semanticTokens = {
  "surface.canvas": "{color.neutral.950}",
  "surface.primary": "{color.neutral.900}",
  "surface.secondary": "{color.neutral.800}",
  "surface.raised": "{color.neutral.800}",

  "text.primary": "{color.neutral.0}",
  "text.secondary": "{color.neutral.200}",
  "text.muted": "{color.neutral.400}",

  "border.subtle": "{color.neutral.800}",
  "border.strong": "{color.neutral.600}",

  "accent.primary": "{color.gold.400}",
  "accent.interactive": "{color.blue.400}",

  "status.healthy": "{color.green.400}",
  "status.attention": "{color.amber.400}",
  "status.critical": "{color.red.400}",
  "status.informational": "{color.blue.400}",

  "focus.ring": "{color.gold.300}",
} as const satisfies TokenMap;
