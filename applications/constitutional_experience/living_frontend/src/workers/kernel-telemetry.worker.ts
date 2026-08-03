/// <reference lib="webworker" />

import { TemporalDeterminismMonitor } from
  "../runtime/temporal-determinism-monitor";

const monitor = new TemporalDeterminismMonitor(1000 / 120, 128);

self.onmessage = (
  event: MessageEvent<
    | { type: "FRAME"; deltaMs: number; timestamp: number }
    | { type: "PING" }
  >,
): void => {
  if (event.data.type === "PING") {
    self.postMessage({ type: "PONG" });
    return;
  }

  const snapshot = monitor.add(
    event.data.deltaMs,
    event.data.timestamp,
  );
  self.postMessage({
    type: "TEMPORAL_SNAPSHOT",
    snapshot,
  });
};

export {};
