import type { CSSProperties, HTMLAttributes, ReactNode } from "react";
import { tokens, type RadiusToken, type ShadowToken, type SpaceToken } from "../../tokens/tokens";

export type SurfaceVariant = 0 | 1 | 2 | 3;

export interface SurfaceProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
  variant?: SurfaceVariant;
  padding?: SpaceToken;
  radius?: RadiusToken;
  elevation?: ShadowToken;
  interactive?: boolean;
  selected?: boolean;
  disabled?: boolean;
}

export function Surface({
  children,
  variant = 1,
  padding = 4,
  radius = "lg",
  elevation = 0,
  interactive = false,
  selected = false,
  disabled = false,
  style,
  ...rest
}: SurfaceProps) {
  const css: CSSProperties = {
    background: `var(--a-surface-${variant})`,
    color: "var(--a-text-1)",
    border: `1px solid ${selected ? "var(--a-focus)" : "var(--a-border)"}`,
    borderRadius: tokens.radius[radius],
    boxShadow: tokens.shadow[elevation],
    padding: tokens.space[padding],
    opacity: disabled ? 0.55 : 1,
    cursor: interactive && !disabled ? "pointer" : undefined,
    transition: `border-color ${tokens.motion.fast}, box-shadow ${tokens.motion.standard}, transform ${tokens.motion.fast}`,
    ...style
  };

  return (
    <div aria-disabled={disabled || undefined} data-selected={selected || undefined} style={css} {...rest}>
      {children}
    </div>
  );
}
