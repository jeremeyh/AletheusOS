import { motion } from "motion/react";

export function RoutePending({
  label = "Resolving workspace",
}: {
  readonly label?: string;
}) {
  return (
    <main className="nimble-route-state">
      <motion.div
        className="nimble-route-state__core"
        animate={{
          rotate: 360,
          scale: [1, 1.12, 1],
        }}
        transition={{
          rotate: {
            duration: 2.6,
            repeat: Number.POSITIVE_INFINITY,
            ease: "linear",
          },
          scale: {
            duration: 1.8,
            repeat: Number.POSITIVE_INFINITY,
            ease: "easeInOut",
          },
        }}
        aria-hidden="true"
      >
        <span />
        <span />
        <span />
      </motion.div>

      <strong>{label}</strong>
      <p>
        Nimble is preserving context while the requested state is loaded.
      </p>
    </main>
  );
}
