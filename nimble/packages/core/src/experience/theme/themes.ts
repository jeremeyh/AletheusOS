import type { ExperienceTheme } from "./contracts";

export const darkTheme: ExperienceTheme = {
  id: "aletheus.dark",
  name: "Aletheus Dark",
  version: "0.1.0",
  variant: "dark",
  tokens: {
    "surface.canvas": "{color.neutral.950}",
    "surface.primary": "{color.neutral.900}",
    "surface.secondary": "{color.neutral.800}",
    "text.primary": "{color.neutral.0}",
    "text.secondary": "{color.neutral.200}",
  },
};

export const lightTheme: ExperienceTheme = {
  id: "aletheus.light",
  name: "Aletheus Light",
  version: "0.1.0",
  variant: "light",
  tokens: {
    "surface.canvas": "{color.neutral.50}",
    "surface.primary": "{color.neutral.0}",
    "surface.secondary": "{color.neutral.100}",
    "text.primary": "{color.neutral.900}",
    "text.secondary": "{color.neutral.600}",
  },
};

export const highContrastTheme: ExperienceTheme = {
  id: "aletheus.high-contrast",
  name: "Aletheus High Contrast",
  version: "0.1.0",
  variant: "high-contrast",
  inherits: "aletheus.dark",
  tokens: {
    "surface.canvas": "#000000",
    "surface.primary": "#000000",
    "text.primary": "#ffffff",
    "text.secondary": "#ffffff",
    "focus.ring": "#ffffff",
  },
};

export const instrumentationTheme: ExperienceTheme = {
  id: "aletheus.instrumentation",
  name: "Aletheus Instrumentation",
  version: "0.1.0",
  variant: "instrumentation",
  inherits: "aletheus.dark",
  tokens: {
    "instrumentation.surface":
      "{color.neutral.900}",
    "instrumentation.border":
      "{color.gold.600}",
    "instrumentation.value":
      "{color.neutral.0}",
    "instrumentation.label":
      "{color.neutral.200}",
  },
};

export const canonicalThemes = [
  darkTheme,
  lightTheme,
  highContrastTheme,
  instrumentationTheme,
] as const;
