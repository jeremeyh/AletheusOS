import { useEffect, useRef } from "react";
import type { PhaseState } from "../types";

export function AdaptiveField({
  phase,
  density,
}: {
  phase: PhaseState;
  density: number;
}) {
  const ref = useRef<HTMLCanvasElement>(null);
  const logoRef = useRef<HTMLImageElement | null>(null);

  useEffect(() => {
    const image = new Image();
    image.src = "/aletheusos-canonical-logo.jpeg";
    image.onload = () => {
      logoRef.current = image;
    };
  }, []);

  useEffect(() => {
    const canvas = ref.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrame = 0;
    let time = 0;

    const resize = () => {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.floor(canvas.clientWidth * dpr);
      canvas.height = Math.floor(canvas.clientHeight * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    };

    const phaseRigidity =
      phase === "Nebular"
        ? 0.25
        : phase === "Fluid Reactive"
          ? 0.52
          : phase === "Quasi-Crystalline"
            ? 0.79
            : 1;

    const draw = () => {
      time += 0.008;
      const width = canvas.clientWidth;
      const height = canvas.clientHeight;
      ctx.clearRect(0, 0, width, height);

      const centerX = width * 0.61;
      const centerY = height * 0.5;
      const image = logoRef.current;

      if (image) {
        const baseSize = Math.min(width, height) * 0.92;
        const breathing = 1 + Math.sin(time * Math.PI * 0.3) * 0.018;
        const size = baseSize * breathing;

        ctx.save();
        ctx.globalAlpha = 0.08 + phaseRigidity * 0.11;
        ctx.filter = `blur(${(1 - phaseRigidity) * 3}px) brightness(${0.85 + phaseRigidity * 0.38})`;
        ctx.drawImage(
          image,
          centerX - size * 0.5,
          centerY - size * 0.5,
          size,
          size,
        );
        ctx.restore();

        const sweepX = centerX + Math.sin(time * 0.7) * size * 0.22;
        const sweep = ctx.createLinearGradient(
          sweepX - 50,
          centerY - size * 0.42,
          sweepX + 50,
          centerY + size * 0.42,
        );
        sweep.addColorStop(0, "rgba(255,255,255,0)");
        sweep.addColorStop(0.48, `rgba(255,229,154,${0.04 + phaseRigidity * 0.05})`);
        sweep.addColorStop(0.52, `rgba(255,255,255,${0.07 + phaseRigidity * 0.08})`);
        sweep.addColorStop(1, "rgba(255,255,255,0)");
        ctx.fillStyle = sweep;
        ctx.fillRect(centerX - size * 0.5, centerY - size * 0.5, size, size);
      }

      const ringCount = 7;
      for (let ring = 0; ring < ringCount; ring += 1) {
        ctx.beginPath();
        ctx.ellipse(
          centerX,
          centerY,
          62 + ring * 20 * density,
          23 + ring * 10 * density,
          time * (ring % 2 === 0 ? 0.22 : -0.16) + ring * 0.4,
          0,
          Math.PI * 2,
        );
        ctx.strokeStyle =
          ring === 2
            ? `rgba(232,196,91,${0.25 + phaseRigidity * 0.42})`
            : `rgba(112,160,255,${0.06 + density * 0.09})`;
        ctx.lineWidth = ring === 2 ? 1.5 : 0.8;
        ctx.stroke();
      }

      const particleCount = Math.floor(42 + density * 76);
      for (let i = 0; i < particleCount; i += 1) {
        const angle = time * (0.48 + (i % 9) * 0.025) + i * 0.61;
        const orbit = (28 + (i % 19) * 6) * (0.7 + density * 0.55);
        const x = centerX + Math.cos(angle) * orbit;
        const y = centerY + Math.sin(angle * 1.31) * orbit * 0.42;

        ctx.beginPath();
        ctx.arc(x, y, 0.7 + (i % 4) * 0.35, 0, Math.PI * 2);
        ctx.fillStyle =
          i % 8 === 0
            ? "rgba(243,207,96,0.94)"
            : "rgba(137,180,255,0.48)";
        ctx.fill();
      }

      animationFrame = requestAnimationFrame(draw);
    };

    resize();
    window.addEventListener("resize", resize);
    draw();

    return () => {
      cancelAnimationFrame(animationFrame);
      window.removeEventListener("resize", resize);
    };
  }, [phase, density]);

  return <canvas ref={ref} className="adaptive-field" aria-hidden="true" />;
}
