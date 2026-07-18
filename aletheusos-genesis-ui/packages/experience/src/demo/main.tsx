import React from "react";
import { createRoot } from "react-dom/client";
import "../styles/theme.css";
import { Grid, Panel, Stack, Surface } from "../index";

function App() {
  return (
    <main style={{ maxWidth: 1180, margin: "0 auto", padding: "2rem" }}>
      <Stack gap={8}>
        <header>
          <p style={{ margin: 0, color: "var(--a-text-2)" }}>AletheusOS™</p>
          <h1 style={{ margin: ".25rem 0 0", fontSize: "2rem" }}>Genesis UI</h1>
        </header>

        <Surface variant={1} padding={6}>
          <Stack gap={3}>
            <strong>Primitive Experience Library™</strong>
            <span style={{ color: "var(--a-text-2)" }}>
              Initial production scaffold for semantic surfaces, layout primitives, and panels.
            </span>
          </Stack>
        </Surface>

        <Grid minColumnWidth="16rem" gap={4}>
          <Panel title="Mission" description="Purpose before implementation.">
            Preserve constitutional intent throughout delivery.
          </Panel>
          <Panel title="Evidence" description="Truth is inspectable.">
            Every recommendation remains traceable to supporting evidence.
          </Panel>
          <Panel title="Runtime" description="Calm operational awareness.">
            Surface only what requires attention.
          </Panel>
        </Grid>
      </Stack>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
