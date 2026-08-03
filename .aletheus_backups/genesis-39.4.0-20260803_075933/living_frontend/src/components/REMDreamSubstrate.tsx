import {
  useEffect,
  useRef,
  useState,
  type PointerEvent as ReactPointerEvent,
} from "react";
import { REMRuntime } from "../runtime/rem-runtime";
import type { REMRuntimeState } from "../runtime/rem-types";

export interface REMDreamSubstrateProps {
  crystallized: boolean;
  resonance: number;
  founderMode?: boolean;
  onState?: (state: REMRuntimeState) => void;
}

export function REMDreamSubstrate({
  crystallized,
  resonance,
  founderMode = false,
  onState,
}: REMDreamSubstrateProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const runtimeRef = useRef<REMRuntime | null>(null);
  const frameRef = useRef<number>(0);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas === null) return;

    const context = canvas.getContext("2d", {
      alpha: true,
      desynchronized: true,
    });
    if (context === null) return;

    const runtime = new REMRuntime();
    runtimeRef.current = runtime;

    const resize = (): void => {
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      const width = Math.max(1, canvas.clientWidth);
      const height = Math.max(1, canvas.clientHeight);
      canvas.width = Math.floor(width * ratio);
      canvas.height = Math.floor(height * ratio);
      context.setTransform(ratio, 0, 0, ratio, 0, 0);

      if (!ready) {
        runtime.initialize(width, height);
        setReady(true);
      } else {
        runtime.resize(width, height);
      }
    };

    resize();
    const observer = new ResizeObserver(resize);
    observer.observe(canvas);

    const render = (timestamp: number): void => {
      const state = runtime.update(timestamp);
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;

      context.clearRect(0, 0, width, height);

      const gradient = context.createRadialGradient(
        width * 0.48,
        height * 0.42,
        20,
        width * 0.5,
        height * 0.5,
        Math.max(width, height) * 0.72,
      );
      gradient.addColorStop(0, "rgba(12, 16, 23, 0.22)");
      gradient.addColorStop(0.46, "rgba(5, 8, 13, 0.34)");
      gradient.addColorStop(1, "rgba(2, 3, 6, 0.72)");
      context.fillStyle = gradient;
      context.fillRect(0, 0, width, height);

      const particles = runtime.particles;
      const connectionRadius = runtime.connectionRadius;

      context.globalCompositeOperation = "lighter";

      for (let index = 0; index < particles.length; index += 1) {
        const particle = particles[index];
        const coherence =
          particle.coherence * (0.82 + resonance * 0.18);
        const shimmer =
          Math.sin(timestamp * 0.0017 + particle.seed * 17) * 0.07;
        const alpha =
          Math.max(0.04, 0.12 + coherence * 0.48 + shimmer);

        context.beginPath();
        context.arc(
          particle.x,
          particle.y,
          particle.size * (0.86 + coherence * 0.42),
          0,
          Math.PI * 2,
        );

        if (coherence > 0.48) {
          context.fillStyle =
            `rgba(231, 195, 95, ${alpha.toFixed(3)})`;
        } else {
          context.fillStyle =
            `rgba(97, 215, 255, ${alpha.toFixed(3)})`;
        }
        context.fill();

        for (
          let neighborIndex = index + 1;
          neighborIndex < particles.length;
          neighborIndex += 1
        ) {
          const neighbor = particles[neighborIndex];
          const dx = particle.x - neighbor.x;
          const dy = particle.y - neighbor.y;
          const distanceSquared = dx * dx + dy * dy;

          if (distanceSquared < connectionRadius * connectionRadius) {
            const distance = Math.sqrt(distanceSquared);
            const edgeAlpha =
              (1 - distance / connectionRadius) *
              (0.025 + coherence * 0.095);

            context.beginPath();
            context.moveTo(particle.x, particle.y);
            context.lineTo(neighbor.x, neighbor.y);
            context.strokeStyle = coherence > 0.55
              ? `rgba(231, 195, 95, ${edgeAlpha.toFixed(3)})`
              : `rgba(97, 215, 255, ${edgeAlpha.toFixed(3)})`;
            context.lineWidth = founderMode ? 0.8 : 0.52;
            context.stroke();
          }
        }
      }

      context.globalCompositeOperation = "source-over";
      onState?.(state);
      frameRef.current = requestAnimationFrame(render);
    };

    frameRef.current = requestAnimationFrame(render);

    return () => {
      observer.disconnect();
      cancelAnimationFrame(frameRef.current);
      runtimeRef.current = null;
    };
  }, [founderMode, onState, ready, resonance]);

  useEffect(() => {
    const runtime = runtimeRef.current;
    if (runtime === null) return;
    if (crystallized) runtime.crystallize(0.94);
    else runtime.dissolve();
  }, [crystallized]);

  const pointerMove = (
    event: ReactPointerEvent<HTMLCanvasElement>,
  ): void => {
    const rect = event.currentTarget.getBoundingClientRect();
    runtimeRef.current?.setPointer({
      x: event.clientX - rect.left,
      y: event.clientY - rect.top,
      active: true,
    });
  };

  const pointerLeave = (): void => {
    runtimeRef.current?.setPointer({
      x: -1000,
      y: -1000,
      active: false,
    });
  };

  return (
    <canvas
      ref={canvasRef}
      className="rem-dream-substrate"
      aria-hidden="true"
      onPointerMove={pointerMove}
      onPointerLeave={pointerLeave}
    />
  );
}
