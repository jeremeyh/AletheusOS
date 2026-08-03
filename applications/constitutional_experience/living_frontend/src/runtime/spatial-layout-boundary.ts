export interface SpatialBody {
  id: string;
  width: number;
  height: number;
  preferredX: number;
  preferredY: number;
  mass: number;
}

export interface SpatialPlacement {
  id: string;
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface SpatialLayoutSolver {
  solve(
    bodies: readonly SpatialBody[],
    viewportWidth: number,
    viewportHeight: number,
  ): readonly SpatialPlacement[];
}
