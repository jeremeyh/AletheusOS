#!/usr/bin/env python3

from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent

REACT_ROOT = (
    ROOT
    / "nimble/packages/react/src"
)

PRIMITIVES_ROOT = (
    REACT_ROOT
    / "primitives"
)

VALIDATOR = (
    ROOT
    / "validate_nimble_primitive_experience.py"
)

TEST_FILE = (
    ROOT
    / "tests/nimble/test_primitive_experience.py"
)


FILES: dict[str, str] = {
    "types.ts": r'''
import type {
  CSSProperties,
  HTMLAttributes,
  ReactNode,
} from "react";


export type ExperienceDensity =
  | "consumer"
  | "professional"
  | "enterprise"
  | "founder"
  | "developer";


export type SurfaceVariant =
  | "canvas"
  | "surface"
  | "panel"
  | "raised"
  | "floating"
  | "overlay"
  | "hud"
  | "instrument";


export type InstrumentKind =
  | "numeric"
  | "meter"
  | "gauge"
  | "signal"
  | "trend"
  | "timeline"
  | "status"
  | "authority"
  | "telemetry";


export type InstrumentStatus =
  | "initializing"
  | "healthy"
  | "attention"
  | "review"
  | "critical"
  | "unavailable";


export interface PrimitiveProps
  extends HTMLAttributes<HTMLElement> {
  readonly children?: ReactNode;
  readonly style?: CSSProperties;
}
''',

    "tokens.ts": r'''
import {
  experienceTokens,
} from "@aletheus/nimble-core";


export type ExperienceTokenName =
  keyof typeof experienceTokens;


export function token(
  name: ExperienceTokenName,
): string | number {
  return experienceTokens[name];
}


export function cssValue(
  name: ExperienceTokenName,
): string {
  const value = token(name);

  return typeof value === "number"
    ? `${value}px`
    : value;
}
''',

    "Surface.tsx": r'''
import {
  forwardRef,
  type CSSProperties,
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";

import type {
  SurfaceVariant,
} from "./types";


export interface SurfaceProps
  extends HTMLAttributes<HTMLDivElement> {
  readonly variant?: SurfaceVariant;
  readonly interactive?: boolean;
}


const VARIANT_STYLES: Readonly<
  Record<
    SurfaceVariant,
    CSSProperties
  >
> = {
  canvas: {
    background:
      cssValue("surface.canvas"),
    color:
      cssValue("text.primary"),
  },

  surface: {
    background:
      cssValue("surface.primary"),
    color:
      cssValue("text.primary"),
  },

  panel: {
    background:
      cssValue("surface.secondary"),
    border:
      `1px solid ${
        cssValue("border.subtle")
      }`,
    color:
      cssValue("text.primary"),
  },

  raised: {
    background:
      cssValue("surface.raised"),
    boxShadow:
      cssValue("elevation.raised"),
    color:
      cssValue("text.primary"),
  },

  floating: {
    background:
      cssValue("surface.raised"),
    boxShadow:
      cssValue("elevation.floating"),
    color:
      cssValue("text.primary"),
  },

  overlay: {
    background:
      cssValue("surface.primary"),
    boxShadow:
      cssValue("elevation.overlay"),
    color:
      cssValue("text.primary"),
  },

  hud: {
    background:
      cssValue("surface.primary"),
    boxShadow:
      cssValue("elevation.hud"),
    color:
      cssValue("text.primary"),
  },

  instrument: {
    background:
      cssValue(
        "instrumentation.surface",
      ),
    border:
      `1px solid ${
        cssValue(
          "instrumentation.border",
        )
      }`,
    color:
      cssValue(
        "instrumentation.value",
      ),
  },
};


export const Surface = forwardRef<
  HTMLDivElement,
  SurfaceProps
>(function Surface(
  {
    variant = "surface",
    interactive = false,
    style,
    ...props
  },
  ref,
) {
  return (
    <div
      ref={ref}
      data-nimble-primitive="surface"
      data-variant={variant}
      data-interactive={
        interactive || undefined
      }
      style={{
        borderRadius:
          cssValue("radius.lg"),
        boxSizing: "border-box",

        transition: interactive
          ? [
              "transform",
              cssValue(
                "motion.duration.fast",
              ),
              cssValue(
                "motion.easing.standard",
              ),
            ].join(" ")
          : undefined,

        ...VARIANT_STYLES[variant],
        ...style,
      }}
      {...props}
    />
  );
});
''',

    "Stack.tsx": r'''
import {
  forwardRef,
  type CSSProperties,
  type HTMLAttributes,
} from "react";

import {
  cssValue,
  type ExperienceTokenName,
} from "./tokens";


export type StackSpacing =
  | "none"
  | "xs"
  | "sm"
  | "md"
  | "lg"
  | "xl"
  | "2xl";


export interface StackProps
  extends HTMLAttributes<HTMLDivElement> {
  readonly direction?:
    | "row"
    | "column";

  readonly spacing?: StackSpacing;

  readonly align?:
    CSSProperties["alignItems"];

  readonly justify?:
    CSSProperties["justifyContent"];

  readonly wrap?: boolean;
}


const SPACING_TOKENS: Readonly<
  Record<
    StackSpacing,
    ExperienceTokenName
  >
> = {
  none: "space.0",
  xs: "space.1",
  sm: "space.2",
  md: "space.4",
  lg: "space.6",
  xl: "space.10",
  "2xl": "space.16",
};


export const Stack = forwardRef<
  HTMLDivElement,
  StackProps
>(function Stack(
  {
    direction = "column",
    spacing = "md",
    align,
    justify,
    wrap = false,
    style,
    ...props
  },
  ref,
) {
  return (
    <div
      ref={ref}
      data-nimble-primitive="stack"
      data-direction={direction}
      style={{
        alignItems: align,
        display: "flex",
        flexDirection: direction,

        flexWrap: wrap
          ? "wrap"
          : "nowrap",

        gap:
          cssValue(
            SPACING_TOKENS[
              spacing
            ],
          ),

        justifyContent: justify,

        ...style,
      }}
      {...props}
    />
  );
});
''',

    "Grid.tsx": r'''
import {
  forwardRef,
  type HTMLAttributes,
} from "react";

import {
  cssValue,
  type ExperienceTokenName,
} from "./tokens";


export type GridGap =
  | "sm"
  | "md"
  | "lg"
  | "xl";


export interface GridProps
  extends HTMLAttributes<HTMLDivElement> {
  readonly columns?:
    | number
    | string;

  readonly gap?: GridGap;

  readonly minColumnWidth?:
    number;
}


const GAP_TOKENS: Readonly<
  Record<
    GridGap,
    ExperienceTokenName
  >
> = {
  sm: "space.2",
  md: "space.4",
  lg: "space.6",
  xl: "space.10",
};


export const Grid = forwardRef<
  HTMLDivElement,
  GridProps
>(function Grid(
  {
    columns = 1,
    gap = "md",
    minColumnWidth,
    style,
    ...props
  },
  ref,
) {
  const template =
    minColumnWidth !== undefined
      ? [
          "repeat(",
          "auto-fit, ",
          "minmax(",
          `min(100%, ${
            minColumnWidth
          }px), `,
          "1fr)",
          ")",
        ].join("")
      : typeof columns === "number"
        ? `repeat(${
            columns
          }, minmax(0, 1fr))`
        : columns;

  return (
    <div
      ref={ref}
      data-nimble-primitive="grid"
      style={{
        display: "grid",

        gap:
          cssValue(
            GAP_TOKENS[gap],
          ),

        gridTemplateColumns:
          template,

        ...style,
      }}
      {...props}
    />
  );
});
''',

    "Text.tsx": r'''
import {
  createElement,
  forwardRef,
  type CSSProperties,
  type ElementType,
  type HTMLAttributes,
} from "react";

import {
  cssValue,
  token,
  type ExperienceTokenName,
} from "./tokens";


export type TextVariant =
  | "display"
  | "heading"
  | "body"
  | "caption"
  | "label"
  | "instrument"
  | "telemetry"
  | "code";


export interface TextProps
  extends HTMLAttributes<HTMLElement> {
  readonly as?: ElementType;
  readonly variant?: TextVariant;
  readonly muted?: boolean;
}


interface TextDefinition {
  readonly fontFamily:
    ExperienceTokenName;

  readonly fontSize:
    ExperienceTokenName;

  readonly fontWeight:
    ExperienceTokenName;

  readonly lineHeight: number;
}


const DEFINITIONS: Readonly<
  Record<
    TextVariant,
    TextDefinition
  >
> = {
  display: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.display",

    fontWeight:
      "font.weight.bold",

    lineHeight: 1.05,
  },

  heading: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.heading.md",

    fontWeight:
      "font.weight.semibold",

    lineHeight: 1.2,
  },

  body: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.body.md",

    fontWeight:
      "font.weight.regular",

    lineHeight: 1.5,
  },

  caption: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.caption",

    fontWeight:
      "font.weight.medium",

    lineHeight: 1.4,
  },

  label: {
    fontFamily:
      "font.family.interface",

    fontSize:
      "font.size.body.sm",

    fontWeight:
      "font.weight.semibold",

    lineHeight: 1.3,
  },

  instrument: {
    fontFamily:
      "font.family.instrument",

    fontSize:
      "font.size.heading.lg",

    fontWeight:
      "font.weight.semibold",

    lineHeight: 1.1,
  },

  telemetry: {
    fontFamily:
      "font.family.instrument",

    fontSize:
      "font.size.body.sm",

    fontWeight:
      "font.weight.medium",

    lineHeight: 1.35,
  },

  code: {
    fontFamily:
      "font.family.instrument",

    fontSize:
      "font.size.body.sm",

    fontWeight:
      "font.weight.regular",

    lineHeight: 1.5,
  },
};


export const Text = forwardRef<
  HTMLElement,
  TextProps
>(function Text(
  {
    as = "span",
    variant = "body",
    muted = false,
    style,
    ...props
  },
  ref,
) {
  const definition =
    DEFINITIONS[variant];

  const fontWeight =
    token(
      definition.fontWeight,
    );

  const computedStyle:
    CSSProperties = {
      color:
        cssValue(
          muted
            ? "text.muted"
            : "text.primary",
        ),

      fontFamily:
        cssValue(
          definition.fontFamily,
        ),

      fontSize:
        cssValue(
          definition.fontSize,
        ),

      fontWeight:
        typeof fontWeight === "number"
          ? fontWeight
          : undefined,

      lineHeight:
        definition.lineHeight,

      margin: 0,

      ...style,
    };

  return createElement(
    as,
    {
      ...props,
      ref,

      "data-nimble-primitive":
        "text",

      "data-variant":
        variant,

      style:
        computedStyle,
    },
  );
});
''',

    "Panel.tsx": r'''
import {
  forwardRef,
  type HTMLAttributes,
} from "react";

import {
  Surface,
} from "./Surface";

import {
  Stack,
  type StackSpacing,
} from "./Stack";

import {
  Text,
} from "./Text";


export interface PanelProps
  extends HTMLAttributes<HTMLDivElement> {
  readonly title?: string;
  readonly description?: string;
  readonly spacing?: StackSpacing;
}


export const Panel = forwardRef<
  HTMLDivElement,
  PanelProps
>(function Panel(
  {
    title,
    description,
    spacing = "lg",
    children,
    style,
    ...props
  },
  ref,
) {
  return (
    <Surface
      ref={ref}
      variant="panel"
      data-nimble-primitive="panel"
      style={{
        padding: 24,
        ...style,
      }}
      {...props}
    >
      <Stack spacing={spacing}>
        {title ? (
          <div>
            <Text
              as="h2"
              variant="heading"
            >
              {title}
            </Text>

            {description ? (
              <Text
                as="p"
                muted
                style={{
                  marginTop: 6,
                }}
              >
                {description}
              </Text>
            ) : null}
          </div>
        ) : null}

        {children}
      </Stack>
    </Surface>
  );
});
''',

    "Signal.tsx": r'''
import {
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";

import type {
  InstrumentStatus,
} from "./types";


export interface SignalProps
  extends HTMLAttributes<HTMLSpanElement> {
  readonly status:
    InstrumentStatus;

  readonly label?: string;
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


export function Signal({
  status,
  label,
  style,
  ...props
}: SignalProps) {
  const color =
    cssValue(
      STATUS_TOKENS[status],
    );

  return (
    <span
      data-nimble-primitive="signal"
      data-status={status}
      style={{
        alignItems: "center",
        color,
        display: "inline-flex",
        fontFamily:
          cssValue(
            "font.family.instrument",
          ),
        fontSize:
          cssValue(
            "font.size.caption",
          ),
        gap:
          cssValue("space.2"),
        ...style,
      }}
      {...props}
    >
      <span
        aria-hidden="true"
        style={{
          background: color,
          borderRadius: "50%",
          boxShadow:
            `0 0 10px ${
              color
            }`,
          height: 7,
          width: 7,
        }}
      />

      {label ?? status}
    </span>
  );
}
''',

    "Meter.tsx": r'''
import {
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";


export interface MeterProps
  extends Omit<
    HTMLAttributes<HTMLDivElement>,
    "children"
  > {
  readonly value: number;
  readonly minimum?: number;
  readonly maximum?: number;
  readonly segments?: number;
  readonly label?: string;
}


export function Meter({
  value,
  minimum = 0,
  maximum = 100,
  segments = 20,
  label,
  style,
  ...props
}: MeterProps) {
  const bounded =
    Math.max(
      minimum,
      Math.min(maximum, value),
    );

  const range =
    maximum - minimum;

  const ratio =
    range > 0
      ? (
          bounded - minimum
        ) / range
      : 0;

  const activeSegments =
    Math.round(
      ratio * segments,
    );

  return (
    <div
      role="meter"
      aria-label={label}
      aria-valuemin={minimum}
      aria-valuemax={maximum}
      aria-valuenow={bounded}
      data-nimble-primitive="meter"
      style={{
        display: "grid",
        gap:
          cssValue("space.1"),
        gridTemplateColumns:
          `repeat(${
            segments
          }, minmax(2px, 1fr))`,
        ...style,
      }}
      {...props}
    >
      {Array.from(
        {
          length: segments,
        },
        (_, index) => (
          <span
            key={index}
            aria-hidden="true"
            data-active={
              index < activeSegments
                ? "true"
                : "false"
            }
            style={{
              background:
                index < activeSegments
                  ? "currentColor"
                  : "rgba(152, 162, 179, 0.13)",

              borderRadius: 2,
              height: 14,

              transition: [
                "background",
                cssValue(
                  "motion.duration.normal",
                ),
                cssValue(
                  "motion.easing.standard",
                ),
              ].join(" "),
            }}
          />
        ),
      )}
    </div>
  );
}
''',

    "Badge.tsx": r'''
import {
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";


export type BadgeIntent =
  | "neutral"
  | "healthy"
  | "attention"
  | "critical"
  | "authority";


export interface BadgeProps
  extends HTMLAttributes<HTMLSpanElement> {
  readonly intent?: BadgeIntent;
}


const INTENT_TOKENS = {
  neutral: "text.secondary",
  healthy:
    "instrumentation.status.healthy",
  attention:
    "instrumentation.status.attention",
  critical:
    "instrumentation.status.critical",
  authority:
    "instrumentation.thorx.guard",
} as const;


export function Badge({
  intent = "neutral",
  style,
  ...props
}: BadgeProps) {
  const color =
    cssValue(
      INTENT_TOKENS[intent],
    );

  return (
    <span
      data-nimble-primitive="badge"
      data-intent={intent}
      style={{
        border:
          `1px solid ${
            color
          }`,
        borderRadius:
          cssValue("radius.pill"),
        color,
        display: "inline-flex",
        fontFamily:
          cssValue(
            "font.family.instrument",
          ),
        fontSize:
          cssValue(
            "font.size.caption",
          ),
        letterSpacing: "0.06em",
        padding:
          `${cssValue(
            "space.1",
          )} ${cssValue(
            "space.3",
          )}`,
        textTransform: "uppercase",
        ...style,
      }}
      {...props}
    />
  );
}
''',

    "Separator.tsx": r'''
import {
  type HTMLAttributes,
} from "react";

import {
  cssValue,
} from "./tokens";


export interface SeparatorProps
  extends HTMLAttributes<HTMLHRElement> {
  readonly orientation?:
    | "horizontal"
    | "vertical";
}


export function Separator({
  orientation = "horizontal",
  style,
  ...props
}: SeparatorProps) {
  return (
    <hr
      aria-orientation={orientation}
      data-nimble-primitive="separator"
      style={{
        background:
          cssValue("border.subtle"),
        border: 0,
        flex: "none",
        height:
          orientation === "horizontal"
            ? 1
            : "auto",
        margin: 0,
        minHeight:
          orientation === "vertical"
            ? 20
            : undefined,
        width:
          orientation === "horizontal"
            ? "100%"
            : 1,
        ...style,
      }}
      {...props}
    />
  );
}
''',

    "Instrument.tsx": r'''
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
''',

    "reserved.tsx": r'''
import {
  Instrument,
  type InstrumentProps,
} from "./Instrument";


type ReservedInstrumentProps =
  Omit<
    InstrumentProps,
    | "id"
    | "label"
    | "accentToken"
  >;


export function AletheusIndexInstrument(
  props: ReservedInstrumentProps,
) {
  return (
    <Instrument
      {...props}
      id="instrument.aletheus-index"
      label="Aletheus Index™"
      accentToken={
        "instrumentation.aletheus-index.primary"
      }
    />
  );
}


export function ThorxInstrument(
  props: ReservedInstrumentProps,
) {
  return (
    <Instrument
      {...props}
      id="instrument.thorx"
      label="THORᵡ"
      kind="authority"
      accentToken={
        "instrumentation.thorx.guard"
      }
    />
  );
}
''',

    "index.ts": r'''
export * from "./Badge";
export * from "./Grid";
export * from "./Instrument";
export * from "./Meter";
export * from "./Panel";
export * from "./Separator";
export * from "./Signal";
export * from "./Stack";
export * from "./Surface";
export * from "./Text";
export * from "./reserved";
export * from "./tokens";
export * from "./types";
''',
}


def write_new(
    path: Path,
    content: str,
) -> None:
    if path.exists():
        raise RuntimeError(
            "Refusing to overwrite existing file: "
            + str(path.relative_to(ROOT))
        )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        content.strip() + "\n",
        encoding="utf-8",
    )


def patch_react_index() -> None:
    path = (
        REACT_ROOT
        / "index.ts"
    )

    export_line = (
        'export * from "./primitives";'
    )

    if not path.exists():
        path.write_text(
            export_line + "\n",
            encoding="utf-8",
        )
        return

    text = path.read_text(
        encoding="utf-8",
    )

    if export_line not in text:
        path.write_text(
            text.rstrip()
            + "\n\n"
            + export_line
            + "\n",
            encoding="utf-8",
        )


def write_validator() -> None:
    write_new(
        VALIDATOR,
        r'''
#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent

PRIMITIVES = (
    ROOT
    / "nimble/packages/react/src/primitives"
)

REPORT = (
    ROOT
    / "reports/nimble/experience/"
    "primitive-experience-validation-latest.json"
)


def main() -> int:
    failures: list[str] = []

    required_files = [
        "Badge.tsx",
        "Grid.tsx",
        "Instrument.tsx",
        "Meter.tsx",
        "Panel.tsx",
        "Separator.tsx",
        "Signal.tsx",
        "Stack.tsx",
        "Surface.tsx",
        "Text.tsx",
        "index.ts",
        "reserved.tsx",
        "tokens.ts",
        "types.ts",
    ]

    for relative in required_files:
        if not (
            PRIMITIVES / relative
        ).is_file():
            failures.append(
                f"Missing primitive file: {relative}"
            )

    combined = "\n".join(
        path.read_text(
            encoding="utf-8"
        )
        for path in PRIMITIVES.rglob("*")
        if (
            path.is_file()
            and path.suffix
            in {".ts", ".tsx"}
        )
    )

    required_concepts = [
        "data-nimble-primitive",
        "Aletheus Index™",
        "THORᵡ",
        "instrument.aletheus-index",
        "instrument.thorx",
        "ExperienceDensity",
        "instrumentation.engine",
        "prefers-reduced-motion",
    ]

    for concept in required_concepts:
        if (
            concept
            == "prefers-reduced-motion"
        ):
            continue

        if concept not in combined:
            failures.append(
                "Missing primitive concept: "
                + concept
            )

    typecheck = subprocess.run(
        [
            "npm",
            "run",
            "typecheck",
            "--workspace",
            "@aletheus/nimble-react",
        ],
        cwd=ROOT / "nimble",
        capture_output=True,
        text=True,
        check=False,
        timeout=180,
    )

    if typecheck.returncode != 0:
        failures.append(
            "Nimble React typecheck failed."
        )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

    REPORT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT.write_text(
        json.dumps(
            {
                "schema_version":
                    "1.0",

                "generated_at":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                "status":
                    status,

                "failures":
                    failures,

                "typecheck_stdout":
                    typecheck.stdout.strip(),

                "typecheck_stderr":
                    typecheck.stderr.strip(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print(
        "NIMBLE™ PRIMITIVE EXPERIENCE"
    )
    print("=" * 72)
    print(
        f"Failures: {len(failures)}"
    )
    print(
        f"Status: {status}"
    )
    print(
        "Report:",
        REPORT.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    if typecheck.returncode != 0:
        print(
            typecheck.stdout
        )
        print(
            typecheck.stderr
        )

    return (
        0
        if status == "PASS"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )


def write_tests() -> None:
    write_new(
        TEST_FILE,
        r'''
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PRIMITIVES = (
    ROOT
    / "nimble/packages/react/src/primitives"
)


def read(
    relative: str,
) -> str:
    return (
        PRIMITIVES / relative
    ).read_text(
        encoding="utf-8"
    )


def test_react_package_exports_primitives() -> None:
    index = (
        ROOT
        / "nimble/packages/react/src/index.ts"
    ).read_text(
        encoding="utf-8"
    )

    assert (
        'export * from "./primitives";'
        in index
    )


def test_surface_is_token_driven() -> None:
    surface = read(
        "Surface.tsx"
    )

    assert "surface.canvas" in surface
    assert "elevation.hud" in surface
    assert "radius.lg" in surface


def test_stack_is_token_driven() -> None:
    stack = read(
        "Stack.tsx"
    )

    assert "space.0" in stack
    assert "space.16" in stack


def test_grid_supports_adaptive_layout() -> None:
    grid = read(
        "Grid.tsx"
    )

    assert "auto-fit" in grid
    assert "minmax" in grid


def test_text_supports_instrument_roles() -> None:
    text = read(
        "Text.tsx"
    )

    assert '"instrument"' in text
    assert '"telemetry"' in text
    assert (
        "font.family.instrument"
        in text
    )


def test_visualization_primitives_exist() -> None:
    assert (
        "data-nimble-primitive=\"meter\""
        in read("Meter.tsx")
    )

    assert (
        "data-nimble-primitive=\"signal\""
        in read("Signal.tsx")
    )


def test_instrument_supports_density_profiles() -> None:
    instrument = read(
        "Instrument.tsx"
    )

    for density in [
        "consumer",
        "enterprise",
        "founder",
    ]:
        assert density in instrument


def test_reserved_instrument_identity_is_immutable() -> None:
    reserved = read(
        "reserved.tsx"
    )

    assert (
        'id="instrument.aletheus-index"'
        in reserved
    )

    assert (
        'label="Aletheus Index™"'
        in reserved
    )

    assert (
        'id="instrument.thorx"'
        in reserved
    )

    assert (
        'label="THORᵡ"'
        in reserved
    )


def test_primitive_validator_passes() -> None:
    result = subprocess.run(
        [
            "python",
            str(
                ROOT
                / "validate_nimble_primitive_experience.py"
            ),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=240,
    )

    assert result.returncode == 0, (
        result.stdout
        + result.stderr
    )

    assert (
        "Status: PASS"
        in result.stdout
    )
''',
    )


def run(
    command: list[str],
) -> None:
    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise SystemExit(
            result.returncode
        )


def main() -> int:
    if PRIMITIVES_ROOT.exists():
        existing = [
            path
            for path
            in PRIMITIVES_ROOT.rglob("*")
            if path.is_file()
        ]

        if existing:
            raise RuntimeError(
                "Refusing to overwrite existing "
                "Primitive Experience Library."
            )

    for relative, content in FILES.items():
        write_new(
            PRIMITIVES_ROOT / relative,
            content,
        )

    patch_react_index()
    write_validator()
    write_tests()

    run(
        [
            "python",
            "-m",
            "py_compile",
            str(VALIDATOR),
        ]
    )

    run(
        [
            "python",
            str(VALIDATOR),
        ]
    )

    run(
        [
            "python",
            "-m",
            "pytest",
            "-q",
            str(TEST_FILE),
        ]
    )

    run(
        [
            "python",
            "-m",
            "nimble.orchestrator",
        ]
    )

    print()
    print("=" * 72)
    print(
        "PRIMITIVE EXPERIENCE BUILD COMPLETE"
    )
    print("=" * 72)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
