import { AnimatePresence, motion } from "motion/react";

import { useNimble } from "../providers/NimbleProvider";

export function ToastRegion() {
  const {
    toasts,
    dismissToast,
  } = useNimble();

  return (
    <div
      className="nimble-toast-region"
      role="region"
      aria-label="Notifications"
      aria-live="polite"
    >
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.button
            key={toast.id}
            className="nimble-toast"
            type="button"
            initial={{
              opacity: 0,
              x: 24,
              scale: 0.96,
            }}
            animate={{
              opacity: 1,
              x: 0,
              scale: 1,
            }}
            exit={{
              opacity: 0,
              x: 24,
              scale: 0.96,
            }}
            onClick={() => {
              dismissToast(toast.id);
            }}
          >
            <strong>{toast.title}</strong>
            <span>{toast.message}</span>
          </motion.button>
        ))}
      </AnimatePresence>
    </div>
  );
}
