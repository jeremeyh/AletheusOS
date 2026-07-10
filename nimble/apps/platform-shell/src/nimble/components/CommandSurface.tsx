import * as Dialog from "@radix-ui/react-dialog";
import { AnimatePresence, motion } from "motion/react";
import {
  useEffect,
  useState,
} from "react";

import { useNimble } from "../providers/NimbleProvider";

const commands = [
  {
    id: "missions",
    icon: "◎",
    title: "Open active missions",
    description: "Navigate to the mission workspace.",
  },
  {
    id: "agents",
    icon: "◇",
    title: "Inspect active agents",
    description: "Show current tasks, confidence, and provenance.",
  },
  {
    id: "health",
    icon: "◉",
    title: "Explain current platform health",
    description: "Reveal checks, evidence, and uncertainty.",
  },
] as const;

export function CommandSurface() {
  const {
    commandOpen,
    setCommandOpen,
    notify,
  } = useNimble();

  const [query, setQuery] = useState("");

  useEffect(() => {
    function handleShortcut(event: KeyboardEvent) {
      if (
        (event.metaKey || event.ctrlKey)
        && event.key.toLowerCase() === "k"
      ) {
        event.preventDefault();
        setCommandOpen(!commandOpen);
      }
    }

    window.addEventListener("keydown", handleShortcut);

    return () => {
      window.removeEventListener("keydown", handleShortcut);
    };
  }, [commandOpen, setCommandOpen]);

  const filteredCommands = commands.filter((command) => {
    const searchable = [
      command.title,
      command.description,
    ]
      .join(" ")
      .toLowerCase();

    return searchable.includes(query.toLowerCase());
  });

  return (
    <Dialog.Root
      open={commandOpen}
      onOpenChange={setCommandOpen}
    >
      <Dialog.Portal>
        <AnimatePresence>
          {commandOpen && (
            <>
              <Dialog.Overlay asChild>
                <motion.div
                  className="nimble-command__overlay"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                />
              </Dialog.Overlay>

              <Dialog.Content asChild>
                <motion.section
                  className="nimble-command"
                  aria-describedby="nimble-command-description"
                  initial={{
                    opacity: 0,
                    y: 28,
                    scale: 0.96,
                  }}
                  animate={{
                    opacity: 1,
                    y: 0,
                    scale: 1,
                  }}
                  exit={{
                    opacity: 0,
                    y: 18,
                    scale: 0.98,
                  }}
                  transition={{
                    type: "spring",
                    stiffness: 260,
                    damping: 24,
                  }}
                >
                  <header className="nimble-command__header">
                    <span aria-hidden="true">✦</span>

                    <Dialog.Title>
                      Ask or command AletheusOS
                    </Dialog.Title>

                    <Dialog.Close asChild>
                      <button
                        className="nimble-icon-button"
                        type="button"
                        aria-label="Close command surface"
                      >
                        ×
                      </button>
                    </Dialog.Close>
                  </header>

                  <Dialog.Description
                    id="nimble-command-description"
                    className="visually-hidden"
                  >
                    Search platform commands and preview their effects.
                  </Dialog.Description>

                  <input
                    className="nimble-command__input"
                    autoFocus
                    value={query}
                    onChange={(event) => {
                      setQuery(event.target.value);
                    }}
                    placeholder="Describe an outcome or enter a command…"
                  />

                  <div className="nimble-command__context">
                    <span>Context: Executive Command</span>
                    <span>Mode: Explain before execute</span>
                  </div>

                  <div className="nimble-command__results">
                    {filteredCommands.map((command) => (
                      <button
                        key={command.id}
                        type="button"
                        onClick={() => {
                          setCommandOpen(false);
                          notify(
                            "Command preview",
                            `${command.title} is ready. No destructive action occurred.`,
                          );
                        }}
                      >
                        <span className="nimble-command__result-icon">
                          {command.icon}
                        </span>

                        <span>
                          <strong>{command.title}</strong>
                          <small>{command.description}</small>
                        </span>

                        <kbd>↵</kbd>
                      </button>
                    ))}

                    {filteredCommands.length === 0 && (
                      <p className="nimble-command__empty">
                        No matching command is registered.
                      </p>
                    )}
                  </div>
                </motion.section>
              </Dialog.Content>
            </>
          )}
        </AnimatePresence>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
