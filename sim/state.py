"""Rocket state representation for the 2D flight simulation."""

from dataclasses import dataclass

import numpy as np


@dataclass
class RocketState:
    """Full state vector for the 2D rocket at a single instant.

    Convention:
      - x: horizontal position (m), positive right
      - y: vertical position (m), positive up
      - theta: pitch angle (rad), 0 = pointing up, positive = clockwise
      - vx, vy: velocity components (m/s)
      - omega: angular velocity (rad/s), positive = clockwise
      - mass: current total mass (kg), decreases as fuel burns
    """

    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    theta: float = 0.0
    omega: float = 0.0
    mass: float = 0.0

    def to_array(self) -> np.ndarray:
        """Pack into a numpy array for the RK4 integrator.

        Order: [x, y, vx, vy, theta, omega, mass]
        """
        return np.array([
            self.x, self.y, self.vx, self.vy,
            self.theta, self.omega, self.mass,
        ])

    @classmethod
    def from_array(cls, arr: np.ndarray) -> "RocketState":
        """Unpack a numpy array back into a RocketState."""
        return cls(
            x=float(arr[0]),
            y=float(arr[1]),
            vx=float(arr[2]),
            vy=float(arr[3]),
            theta=float(arr[4]),
            omega=float(arr[5]),
            mass=float(arr[6]),
        )
