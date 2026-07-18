import type { ReactNode } from "react";
import { Surface } from "../../primitives/Surface/Surface";
import { Stack } from "../../primitives/Stack/Stack";

export interface PanelProps {
  title: string;
  description?: string;
  actions?: ReactNode;
  children: ReactNode;
  footer?: ReactNode;
}

export function Panel({ title, description, actions, children, footer }: PanelProps) {
  return (
    <Surface variant={2} padding={6} radius="lg" elevation={1}>
      <Stack gap={4}>
        <header style={{ display: "flex", justifyContent: "space-between", gap: "1rem", alignItems: "flex-start" }}>
          <div>
            <h2 style={{ margin: 0, fontSize: "1rem", lineHeight: 1.25 }}>{title}</h2>
            {description ? (
              <p style={{ margin: ".35rem 0 0", color: "var(--a-text-2)", fontSize: ".875rem" }}>
                {description}
              </p>
            ) : null}
          </div>
          {actions}
        </header>
        <div>{children}</div>
        {footer ? <footer style={{ borderTop: "1px solid var(--a-border)", paddingTop: "1rem" }}>{footer}</footer> : null}
      </Stack>
    </Surface>
  );
}
