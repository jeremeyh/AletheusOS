/// <reference lib="webworker" />

import { REMRuntime } from "../runtime/rem-runtime";

const runtime = new REMRuntime();

self.onmessage = (
  event: MessageEvent<
    | { type: "INITIALIZE"; width: number; height: number }
    | { type: "RESIZE"; width: number; height: number }
    | { type: "CRYSTALLIZE"; intensity?: number }
    | { type: "DISSOLVE" }
    | { type: "STEP"; timestamp: number }
  >,
): void => {
  const message = event.data;

  switch (message.type) {
    case "INITIALIZE":
      runtime.initialize(message.width, message.height);
      break;
    case "RESIZE":
      runtime.resize(message.width, message.height);
      break;
    case "CRYSTALLIZE":
      runtime.crystallize(message.intensity);
      break;
    case "DISSOLVE":
      runtime.dissolve();
      break;
    case "STEP":
      self.postMessage({
        type: "STATE",
        state: runtime.update(message.timestamp),
        particles: runtime.particles,
      });
      break;
  }
};

export {};
