import type { TokenMap } from "./types";

export const colorTokens = {
  "color.neutral.0": "#ffffff",
  "color.neutral.50": "#f7f8fa",
  "color.neutral.100": "#eceff3",
  "color.neutral.200": "#d8dde5",
  "color.neutral.400": "#98a2b3",
  "color.neutral.600": "#475467",
  "color.neutral.800": "#1d2939",
  "color.neutral.900": "#101828",
  "color.neutral.950": "#080d16",

  "color.gold.300": "#e9ca79",
  "color.gold.400": "#d9af48",
  "color.gold.500": "#bd8d22",
  "color.gold.600": "#956c17",

  "color.blue.400": "#53a6ff",
  "color.blue.500": "#2f85e8",
  "color.cyan.400": "#43d6dc",
  "color.green.400": "#42cf8a",
  "color.amber.400": "#f2b94b",
  "color.red.400": "#f36b6b",
  "color.violet.400": "#a98bff",
} as const satisfies TokenMap;

export const spacingTokens = {
  "space.0": 0,
  "space.1": 4,
  "space.2": 8,
  "space.3": 12,
  "space.4": 16,
  "space.5": 20,
  "space.6": 24,
  "space.8": 32,
  "space.10": 40,
  "space.12": 48,
  "space.16": 64,
  "space.20": 80,
  "space.24": 96,
} as const satisfies TokenMap;

export const radiusTokens = {
  "radius.none": 0,
  "radius.sm": 6,
  "radius.md": 10,
  "radius.lg": 16,
  "radius.xl": 24,
  "radius.pill": 999,
} as const satisfies TokenMap;

export const typographyTokens = {
  "font.family.interface":
    'Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif',
  "font.family.instrument":
    '"IBM Plex Mono", "SFMono-Regular", Consolas, monospace',

  "font.size.caption": 12,
  "font.size.body.sm": 14,
  "font.size.body.md": 16,
  "font.size.body.lg": 18,
  "font.size.heading.sm": 20,
  "font.size.heading.md": 24,
  "font.size.heading.lg": 32,
  "font.size.display": 48,

  "font.weight.regular": 400,
  "font.weight.medium": 500,
  "font.weight.semibold": 600,
  "font.weight.bold": 700,
} as const satisfies TokenMap;

export const motionTokens = {
  "motion.duration.instant": 0,
  "motion.duration.fast": 120,
  "motion.duration.normal": 220,
  "motion.duration.slow": 360,
  "motion.duration.deliberation": 720,
  "motion.duration.authorization": 480,
  "motion.duration.pulse": 1200,
  "motion.duration.heartbeat": 1800,

  "motion.easing.standard":
    "cubic-bezier(0.2, 0, 0, 1)",
  "motion.easing.enter":
    "cubic-bezier(0, 0, 0.2, 1)",
  "motion.easing.exit":
    "cubic-bezier(0.4, 0, 1, 1)",
} as const satisfies TokenMap;

export const elevationTokens = {
  "elevation.surface": "none",
  "elevation.raised":
    "0 8px 24px rgba(8, 13, 22, 0.12)",
  "elevation.floating":
    "0 16px 40px rgba(8, 13, 22, 0.18)",
  "elevation.overlay":
    "0 24px 72px rgba(8, 13, 22, 0.28)",
  "elevation.hud":
    "0 0 0 1px rgba(217, 175, 72, 0.18), 0 18px 52px rgba(8, 13, 22, 0.32)",
} as const satisfies TokenMap;

export const breakpointTokens = {
  "breakpoint.sm": 640,
  "breakpoint.md": 768,
  "breakpoint.lg": 1024,
  "breakpoint.xl": 1280,
  "breakpoint.2xl": 1536,
} as const satisfies TokenMap;

export const primitiveTokens = {
  ...colorTokens,
  ...spacingTokens,
  ...radiusTokens,
  ...typographyTokens,
  ...motionTokens,
  ...elevationTokens,
  ...breakpointTokens,
} as const satisfies TokenMap;
