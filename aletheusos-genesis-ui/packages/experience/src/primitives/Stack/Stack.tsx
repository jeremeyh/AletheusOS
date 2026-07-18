import type { CSSProperties, HTMLAttributes, ReactNode } from "react";
import { tokens, type SpaceToken } from "../../tokens/tokens";

export interface StackProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
  gap?: SpaceToken;
  align?: CSSProperties["alignItems"];
}

export function Stack({ children, gap = 4, align = "stretch", style, ...rest }: StackProps) {
  return (
    <div
      style={{ display: "flex", flexDirection: "column", gap: tokens.space[gap], alignItems: align, ...style }}
      {...rest}
    >
      {children}
    </div>
  );
}
