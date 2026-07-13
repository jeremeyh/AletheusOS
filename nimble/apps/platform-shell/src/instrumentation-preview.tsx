import {
  StrictMode,
} from "react";

import {
  createRoot,
} from "react-dom/client";

import {
  IntelligenceInstrumentationShowcase,
} from "./nimble/showcase/IntelligenceInstrumentationShowcase";


const root =
  document.getElementById(
    "instrumentation-root",
  );


if (!root) {
  throw new Error(
    "Instrumentation preview root is missing.",
  );
}


createRoot(root).render(
  <StrictMode>
    <IntelligenceInstrumentationShowcase />
  </StrictMode>,
);
