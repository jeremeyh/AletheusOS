export type TokenPrimitive = string | number;

export type TokenMap = Readonly<
  Record<string, TokenPrimitive>
>;

export interface TokenDefinition {
  readonly name: string;
  readonly value: TokenPrimitive;
  readonly category: string;
  readonly description?: string;
  readonly reference?: string;
}

export interface TokenValidationResult {
  readonly valid: boolean;
  readonly failures: readonly string[];
  readonly tokenCount: number;
}
