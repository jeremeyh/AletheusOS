import { ThemeRegistry } from "./registry";
import { canonicalThemes } from "./themes";

export * from "./contracts";
export * from "./registry";
export * from "./themes";

export function createThemeRegistry(): ThemeRegistry {
  const registry = new ThemeRegistry();

  for (const theme of canonicalThemes) {
    registry.register(theme);
  }

  registry.activate("aletheus.dark");

  return registry;
}
