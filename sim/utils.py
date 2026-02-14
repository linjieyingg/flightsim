"""Utility functions for the rocket flight simulation."""

import math

import numpy as np


def clamp(value: float, lo: float, hi: float) -> float:
    """Clamp a value to the range [lo, hi]."""
    return max(lo, min(hi, value))


def wrap_angle(theta: float) -> float:
    """Wrap an angle to [-pi, pi]."""
    return (theta + math.pi) % (2.0 * math.pi) - math.pi


def rotation_matrix(theta: float) -> np.ndarray:
    """2x2 rotation matrix: body frame -> world frame.

    Body frame convention (theta=0, rocket pointing up):
      - body x-axis = along rocket axis (nose direction) -> world +y
      - body y-axis = perpendicular rightward -> world +x

    Args:
        theta: Pitch angle in radians (0 = up, positive = clockwise).

    Returns:
        2x2 numpy array.
    """
    c, s = math.cos(theta), math.sin(theta)
    return np.array([[-s, c],
                     [c, s]])


def body_to_world(vec_body: np.ndarray, theta: float) -> np.ndarray:
    """Transform a 2D vector from body frame to world frame.

    Args:
        vec_body: [along_axis, perpendicular] in body frame.
        theta: Pitch angle in radians.

    Returns:
        [world_x, world_y] numpy array.
    """
    return rotation_matrix(theta) @ vec_body
