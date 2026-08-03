export interface ConstraintBodyState {
  id: string;
  x: number;
  y: number;
  velocityX: number;
  velocityY: number;
  angle: number;
  angularVelocity: number;
  mass: number;
  friction: number;
  restitution: number;
}

export interface ConstraintPhysicsEngine {
  add(body: ConstraintBodyState): void;
  remove(id: string): void;
  step(deltaSeconds: number): readonly ConstraintBodyState[];
}
