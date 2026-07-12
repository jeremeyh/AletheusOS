import type {
  TokenDefinition,
  TokenValidationResult,
} from "./types";

const TOKEN_NAME_PATTERN =
  /^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$/;

const REFERENCE_PATTERN = /^\{([^{}]+)\}$/;

export function validateTokens(
  tokens: readonly TokenDefinition[],
): TokenValidationResult {
  const failures: string[] = [];
  const names = new Set<string>();

  for (const token of tokens) {
    if (!TOKEN_NAME_PATTERN.test(token.name)) {
      failures.push(
        `Invalid token name: ${token.name}`,
      );
    }

    if (names.has(token.name)) {
      failures.push(
        `Duplicate token name: ${token.name}`,
      );
    }

    names.add(token.name);
  }

  for (const token of tokens) {
    if (typeof token.value !== "string") {
      continue;
    }

    const match = token.value.match(
      REFERENCE_PATTERN,
    );

    const reference = match?.[1];

    if (
      reference &&
      !names.has(reference)
    ) {
      failures.push(
        `Unresolved token reference: ${token.name} -> ${reference}`,
      );
    }
  }

  return {
    valid: failures.length === 0,
    failures,
    tokenCount: tokens.length,
  };
}
