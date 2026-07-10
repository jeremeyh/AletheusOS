import { motion, useReducedMotion } from "motion/react";

const orbs = [
  {
    id: "gold",
    className: "nimble-orb nimble-orb--gold",
    duration: 9,
  },
  {
    id: "violet",
    className: "nimble-orb nimble-orb--violet",
    duration: 12,
  },
  {
    id: "cyan",
    className: "nimble-orb nimble-orb--cyan",
    duration: 15,
  },
] as const;

export function MotionEnvironment() {
  const reducedMotion = useReducedMotion();

  return (
    <div className="nimble-environment" aria-hidden="true">
      {orbs.map((orb, index) => (
        <motion.div
          key={orb.id}
          className={orb.className}
          animate={
            reducedMotion
              ? undefined
              : {
                  x: [0, 26, -14, 0],
                  y: [0, -18, 22, 0],
                  rotate: [0, 8, -6, 0],
                  scale: [1, 1.08, 0.96, 1],
                }
          }
          transition={{
            duration: orb.duration,
            delay: index * -2,
            repeat: Number.POSITIVE_INFINITY,
            ease: "easeInOut",
          }}
        />
      ))}

      <div className="nimble-grid" />
    </div>
  );
}
