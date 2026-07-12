import {
  experienceTokens,
} from "@aletheus/nimble-core";


export type ExperienceTokenName =
  keyof typeof experienceTokens;


export function token(
  name: ExperienceTokenName,
): string | number {
  const value = experienceTokens[name];

  if (value === undefined) {
    throw new Error(
      `Unknown experience token: ${name}`,
    );
  }

  return value;
}


export function cssValue(
  name: ExperienceTokenName,
): string {
  const value = token(name);

  return typeof value === "number"
    ? `${value}px`
    : value;
}
