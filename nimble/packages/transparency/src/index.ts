import type {
  NimbleTruthEnvelope,
} from "@aletheus/nimble-core";

export function assertTruthEnvelope(
  value: NimbleTruthEnvelope,
): NimbleTruthEnvelope {
  if (!value.state.trim()) {
    throw new Error("Nimble truth state cannot be empty.");
  }

  if (!value.explanation.trim()) {
    throw new Error(
      "Nimble truth explanation cannot be empty.",
    );
  }

  if (
    value.confidence
    && (
      value.confidence.value < 0
      || value.confidence.value > 1
    )
  ) {
    throw new Error(
      "Nimble confidence must be between 0 and 1.",
    );
  }

  return value;
}
