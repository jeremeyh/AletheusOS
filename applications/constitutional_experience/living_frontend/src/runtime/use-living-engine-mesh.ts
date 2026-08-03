import { useEffect, useRef, useState } from "react";
import {
  createDefaultLivingEngineMesh,
  type LivingEngineMesh,
} from "./living-engine-mesh";
import type { LivingEngineMeshSnapshot } from "./living-engine-mesh-types";

export function useLivingEngineMesh(): LivingEngineMeshSnapshot {
  const meshRef = useRef<LivingEngineMesh | null>(null);
  if (meshRef.current === null) {
    meshRef.current = createDefaultLivingEngineMesh();
  }

  const [snapshot, setSnapshot] = useState(() => meshRef.current!.snapshot());

  useEffect(() => {
    const timer = window.setInterval(() => {
      setSnapshot(meshRef.current!.snapshot());
    }, 500);
    return () => window.clearInterval(timer);
  }, []);

  return snapshot;
}
