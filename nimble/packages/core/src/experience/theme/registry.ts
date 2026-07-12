import type {
  ExperienceTheme,
} from "./contracts";

export class ThemeRegistry {
  readonly #themes = new Map<
    string,
    ExperienceTheme
  >();

  #activeThemeId: string | undefined;

  register(theme: ExperienceTheme): void {
    if (this.#themes.has(theme.id)) {
      throw new Error(
        `Duplicate experience theme: ${theme.id}`,
      );
    }

    this.#themes.set(theme.id, theme);
  }

  resolve(id: string): ExperienceTheme {
    const theme = this.#themes.get(id);

    if (!theme) {
      throw new Error(
        `Unknown experience theme: ${id}`,
      );
    }

    return theme;
  }

  activate(id: string): ExperienceTheme {
    const theme = this.resolve(id);

    this.#activeThemeId = id;

    return theme;
  }

  active(): ExperienceTheme | undefined {
    return this.#activeThemeId
      ? this.resolve(this.#activeThemeId)
      : undefined;
  }

  list(): readonly ExperienceTheme[] {
    return [...this.#themes.values()];
  }
}
