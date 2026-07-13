import type {
  InstrumentState,
  InstrumentationListener,
  InstrumentationSnapshot,
} from "./contracts";

import {
  validateInstrumentState,
} from "./validation";


export class InstrumentationRegistry {
  readonly #instruments = new Map<
    string,
    InstrumentState
  >();

  readonly #listeners = new Set<
    InstrumentationListener
  >();


  register(
    instrument: InstrumentState,
  ): void {
    if (
      this.#instruments.has(
        instrument.id,
      )
    ) {
      throw new Error(
        `Duplicate instrument: ${instrument.id}`,
      );
    }

    const validation =
      validateInstrumentState(
        instrument,
      );

    if (!validation.valid) {
      throw new Error(
        [
          "Instrument validation failed:",
          ...validation.failures,
        ].join("\n"),
      );
    }

    this.#instruments.set(
      instrument.id,
      Object.freeze({
        ...instrument,
      }),
    );

    this.#emit();
  }


  update(
    instrument: InstrumentState,
  ): void {
    if (
      !this.#instruments.has(
        instrument.id,
      )
    ) {
      throw new Error(
        `Unknown instrument: ${instrument.id}`,
      );
    }

    const validation =
      validateInstrumentState(
        instrument,
      );

    if (!validation.valid) {
      throw new Error(
        [
          "Instrument validation failed:",
          ...validation.failures,
        ].join("\n"),
      );
    }

    this.#instruments.set(
      instrument.id,
      Object.freeze({
        ...instrument,
      }),
    );

    this.#emit();
  }


  resolve(
    id: string,
  ): InstrumentState {
    const instrument =
      this.#instruments.get(id);

    if (!instrument) {
      throw new Error(
        `Unknown instrument: ${id}`,
      );
    }

    return instrument;
  }


  has(
    id: string,
  ): boolean {
    return this.#instruments.has(id);
  }


  list(): readonly InstrumentState[] {
    return Object.freeze(
      [
        ...this.#instruments.values(),
      ],
    );
  }


  snapshot(): InstrumentationSnapshot {
    return Object.freeze({
      schemaVersion: "1.0",
      capturedAt:
        new Date().toISOString(),
      instruments: this.list(),
    });
  }


  subscribe(
    listener: InstrumentationListener,
  ): () => void {
    this.#listeners.add(listener);

    listener(this.snapshot());

    return () => {
      this.#listeners.delete(
        listener,
      );
    };
  }


  #emit(): void {
    const snapshot =
      this.snapshot();

    for (
      const listener
      of this.#listeners
    ) {
      listener(snapshot);
    }
  }
}
