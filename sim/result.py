"""Flight data logging for the rocket simulation."""

from dataclasses import dataclass, field
from typing import List

import numpy as np

from sim.state import RocketState


@dataclass
class FlightRecord:
    """A single timestep snapshot for logging.

    Sensor and Kalman fields default to 0.0 and are populated
    in later phases (3+, 4+) without modifying this structure.
    """

    time: float = 0.0
    state: RocketState = field(default_factory=RocketState)
    thrust: float = 0.0
    gimbal_angle: float = 0.0

    # Sensor readings (Phase 3+)
    accel_reading: float = 0.0
    gyro_reading: float = 0.0
    altimeter_reading: float = 0.0
    gps_x_reading: float = 0.0
    gps_y_reading: float = 0.0

    # Kalman filter estimates (Phase 4+)
    estimated_x: float = 0.0
    estimated_y: float = 0.0
    estimated_vx: float = 0.0
    estimated_vy: float = 0.0
    estimated_theta: float = 0.0
    estimated_omega: float = 0.0


@dataclass
class SimulationResult:
    """Collects FlightRecords and provides array accessors for plotting.

    Usage:
        result = SimulationResult()
        result.append(FlightRecord(time=0.0, state=state, thrust=1200.0))
        ...
        times = result.times    # np.ndarray for matplotlib
        altitudes = result.y
    """

    records: List[FlightRecord] = field(default_factory=list)

    def append(self, record: FlightRecord) -> None:
        """Add a timestep record."""
        self.records.append(record)

    # --- Array accessors for visualization (Phase 6) ---

    @property
    def times(self) -> np.ndarray:
        return np.array([r.time for r in self.records])

    @property
    def x(self) -> np.ndarray:
        return np.array([r.state.x for r in self.records])

    @property
    def y(self) -> np.ndarray:
        return np.array([r.state.y for r in self.records])

    @property
    def vx(self) -> np.ndarray:
        return np.array([r.state.vx for r in self.records])

    @property
    def vy(self) -> np.ndarray:
        return np.array([r.state.vy for r in self.records])

    @property
    def theta(self) -> np.ndarray:
        return np.array([r.state.theta for r in self.records])

    @property
    def omega(self) -> np.ndarray:
        return np.array([r.state.omega for r in self.records])

    @property
    def mass(self) -> np.ndarray:
        return np.array([r.state.mass for r in self.records])

    @property
    def thrust(self) -> np.ndarray:
        return np.array([r.thrust for r in self.records])

    @property
    def gimbal(self) -> np.ndarray:
        return np.array([r.gimbal_angle for r in self.records])
