import type {
  ReactNode,
} from "react";

import {
  Meter,
} from "./Meter";

import {
  Signal,
} from "./Signal";

import {
  Stack,
} from "./Stack";

import {
  Surface,
} from "./Surface";

import {
  Text,
} from "./Text";

import {
  cssValue,
  type ExperienceTokenName,
} from "./tokens";

import type {
  ExperienceDensity,
  InstrumentKind,
  InstrumentStatus,
} from "./types";


export interface InstrumentProps {
  readonly id: string;
  readonly label: string;

  readonly value:
    ReactNode;

  readonly kind?:
    InstrumentKind;

  readonly status?:
    InstrumentStatus;

  readonly density?:
    ExperienceDensity;

  readonly detail?:
    ReactNode;

  readonly footer?:
    ReactNode;

  readonly numericValue?:
    number;

  readonly accentToken?:
    ExperienceTokenName;

  readonly className?:
    string;
}


const STATUS_TOKENS = {
  initializing:
    "text.muted",

  healthy:
    "instrumentation.status.healthy",

  attention:
    "instrumentation.status.attention",

  review:
    "instrumentation.status.attention",

  critical:
    "instrumentation.status.critical",

  unavailable:
    "text.muted",
} as const;


export function Instrument({
  id,
  label,
  value,
  kind = "numeric",
  status = "initializing",
  density = "consumer",
  detail,
  footer,
  numericValue,
  accentToken,
  className,
}: InstrumentProps) {
  const accent =
    cssValue(
      accentToken
        ?? STATUS_TOKENS[status],
    );

  return (
    <Surface
      className={className}
      variant="instrument"
      aria-label={label}
      data-nimble-primitive="instrument"
      data-instrument-id={id}
      data-instrument-kind={kind}
      data-density={density}
      data-status={status}
      style={{
        color: accent,

        minHeight:
          density === "founder"
            ? 184
            : density === "enterprise"
              ? 146
              : 112,

        overflow: "hidden",

        padding:
          cssValue(
            density === "founder"
              ? "space.6"
              : "space.4",
          ),

        position: "relative",
      }}
    >
      <div
        aria-hidden="true"
        style={{
          background: accent,
          height: 3,
          inset: "0 0 auto",
          opacity: 0.92,
          position: "absolute",
        }}
      />

      <Stack spacing="sm">
        <Stack
          direction="row"
          align="center"
          justify="space-between"
          spacing="sm"
        >
          <Text
            as="div"
            variant="caption"
            muted
            style={{
              letterSpacing:
                "0.08em",
              textTransform:
                "uppercase",
            }}
          >
            {label}
          </Text>

          <Signal
            status={status}
            aria-label={
              `${label} status: ${
                status
              }`
            }
          />
        </Stack>

        <Text
          as="div"
          variant="instrument"
          style={{
            color:
              cssValue(
                "instrumentation.value",
              ),
          }}
        >
          {value}
        </Text>

        {numericValue !== undefined ? (
          <Meter
            value={numericValue}
            label={`${label} meter`}
          />
        ) : null}

        {density !== "consumer"
          && detail ? (
            <Text
              as="div"
              variant="telemetry"
              muted
            >
              {detail}
            </Text>
          ) : null}

        {density === "founder"
          && footer ? (
            <div>
              {footer}
            </div>
          ) : null}
      </Stack>
    </Surface>
  );
}
