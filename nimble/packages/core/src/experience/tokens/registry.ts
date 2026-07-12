import type {
  TokenDefinition,
  TokenMap,
  TokenPrimitive,
} from "./types";

export class TokenRegistry {
  readonly #tokens = new Map<
    string,
    TokenDefinition
  >();

  register(
    category: string,
    tokens: TokenMap,
  ): void {
    for (const [name, value] of Object.entries(tokens)) {
      if (this.#tokens.has(name)) {
        throw new Error(
          `Duplicate experience token: ${name}`,
        );
      }

      this.#tokens.set(name, {
        name,
        value,
        category,
      });
    }
  }

  resolve(name: string): TokenPrimitive {
    const token = this.#tokens.get(name);

    if (!token) {
      throw new Error(
        `Unknown experience token: ${name}`,
      );
    }

    return token.value;
  }

  has(name: string): boolean {
    return this.#tokens.has(name);
  }

  entries(): readonly TokenDefinition[] {
    return [...this.#tokens.values()];
  }

  snapshot(): Readonly<Record<string, TokenPrimitive>> {
    return Object.freeze(
      Object.fromEntries(
        [...this.#tokens.entries()].map(
          ([name, definition]) => [
            name,
            definition.value,
          ],
        ),
      ),
    );
  }
}
