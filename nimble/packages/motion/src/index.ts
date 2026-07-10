export interface NimbleSpring {
  readonly stiffness: number;
  readonly damping: number;
  readonly mass: number;
}

export const nimbleSprings = {
  responsive: {
    stiffness: 420,
    damping: 34,
    mass: 0.8,
  },
  expressive: {
    stiffness: 260,
    damping: 24,
    mass: 1,
  },
  structural: {
    stiffness: 180,
    damping: 28,
    mass: 1.2,
  },
} satisfies Record<string, NimbleSpring>;
