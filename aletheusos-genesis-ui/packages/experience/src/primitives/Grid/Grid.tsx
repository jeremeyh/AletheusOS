import type { HTMLAttributes, ReactNode } from "react";
import { tokens, type SpaceToken } from "../../tokens/tokens";

export interface GridProps extends HTMLAttributes<HTMLDivElement> {
  children?: ReactNode;
  minColumnWidth?: string;
  gap?: SpaceToken;
}

export function Grid({ children, minColumnWidth = "18rem", gap = 4, style, ...rest }: GridProps) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `repeat(auto-fit, minmax(min(100%, ${minColumnWidth}), 1fr))`,
        gap: tokens.space[gap],
        ...style
      }}
      {...rest}
    >
      {children}
    </div>
  );
}
