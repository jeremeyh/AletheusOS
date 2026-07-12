import type {
  TokenPrimitive,
} from "../tokens";

export type ThemeVariant =
  | "dark"
  | "light"
  | "high-contrast"
  | "instrumentation";

export interface ExperienceTheme {
  readonly id: string;
  readonly name: string;
  readonly version: string;
  readonly variant: ThemeVariant;
  readonly inherits?: string;
  readonly tokens: Readonly<
    Record<string, TokenPrimitive>
  >;
  readonly metadata?: Readonly<
    Record<string, unknown>
  >;
}
