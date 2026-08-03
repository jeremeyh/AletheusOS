import type { MagneticVector } from "../types";

export interface MagneticPhysicsConfig {
  stiffness: number;
  damping: number;
  mass: number;
  magneticStrength: number;
  maxDisplacement: number;
}

export const defaultMagneticPhysicsConfig: MagneticPhysicsConfig = {
  stiffness: 120,
  damping: 20,
  mass: 1,
  magneticStrength: 0.16,
  maxDisplacement: 18,
};

export function integrateMagneticVector(
  current: MagneticVector,
  targetX: number,
  targetY: number,
  deltaSeconds: number,
  config: MagneticPhysicsConfig = defaultMagneticPhysicsConfig,
): MagneticVector {
  const safeDelta = Math.min(Math.max(deltaSeconds, 0), 1 / 20);
  const displacementX = current.x - targetX;
  const displacementY = current.y - targetY;

  const magneticX =
    -Math.sign(displacementX) *
    config.magneticStrength *
    Math.min(Math.abs(displacementX), config.maxDisplacement);
  const magneticY =
    -Math.sign(displacementY) *
    config.magneticStrength *
    Math.min(Math.abs(displacementY), config.maxDisplacement);

  const accelerationX =
    (-config.stiffness * displacementX -
      config.damping * current.velocityX +
      magneticX) /
    config.mass;
  const accelerationY =
    (-config.stiffness * displacementY -
      config.damping * current.velocityY +
      magneticY) /
    config.mass;

  const velocityX = current.velocityX + accelerationX * safeDelta;
  const velocityY = current.velocityY + accelerationY * safeDelta;

  return {
    x: current.x + velocityX * safeDelta,
    y: current.y + velocityY * safeDelta,
    velocityX,
    velocityY,
    accelerationX,
    accelerationY,
  };
}
