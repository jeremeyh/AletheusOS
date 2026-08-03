import { useEffect, useState } from "react";
import {
  LivingExperienceHardwareRuntime,
  type LivingExperienceHardwareState,
} from "./living-experience-hardware-runtime";

const initialState: LivingExperienceHardwareState = {
  initialized: false,
  backend: "canvas2d",
  capabilities: null,
  quality: null,
  workerEnabled: false,
  reason: "Detecting runtime capabilities",
};

export function useHardwareRuntime(): LivingExperienceHardwareState {
  const [state, setState] =
    useState<LivingExperienceHardwareState>(initialState);

  useEffect(() => {
    const runtime = new LivingExperienceHardwareRuntime();
    void runtime.initialize().then(setState);
  }, []);

  return state;
}
