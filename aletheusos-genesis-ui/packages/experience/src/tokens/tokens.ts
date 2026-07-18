export const tokens = {
  color: {
    truth: "#2457D6",
    knowledge: "#B88A1E",
    intelligence: "#6E4AD7",
    success: "#2E8B57",
    warning: "#C47A00",
    risk: "#C43D3D",
    neutral: {
      0: "#FFFFFF",
      50: "#F7F8FA",
      100: "#EEF0F4",
      200: "#D9DDE5",
      500: "#737B8C",
      700: "#394150",
      900: "#151922"
    }
  },
  space: {
    1: "0.25rem",
    2: "0.5rem",
    3: "0.75rem",
    4: "1rem",
    6: "1.5rem",
    8: "2rem",
    10: "2.5rem",
    12: "3rem",
    16: "4rem"
  },
  radius: {
    sm: "0.375rem",
    md: "0.625rem",
    lg: "0.875rem",
    xl: "1.25rem"
  },
  shadow: {
    0: "none",
    1: "0 1px 2px rgba(0,0,0,.06)",
    2: "0 8px 24px rgba(0,0,0,.10)",
    3: "0 16px 48px rgba(0,0,0,.16)"
  },
  motion: {
    fast: "120ms",
    standard: "200ms",
    slow: "320ms"
  }
} as const;

export type SpaceToken = keyof typeof tokens.space;
export type RadiusToken = keyof typeof tokens.radius;
export type ShadowToken = keyof typeof tokens.shadow;
