"""Configuration dataclasses for the rocket flight simulation.

All tunable parameters live here — no magic numbers in the codebase.
"""

import math
from dataclasses import dataclass, field


@dataclass
class RocketConfig:
    """Physical properties of the rocket."""

    dry_mass: float = 50.0              # kg
    fuel_mass: float = 30.0             # kg
    max_thrust: float = 1200.0          # N
    Isp: float = 220.0                  # s  (specific impulse)
    length: float = 2.0                 # m
    diameter: float = 0.15              # m
    drag_coeff: float = 0.4             # dimensionless (Cd)
    moment_of_inertia: float = 80.0     # kg*m^2 (about CoM)
    cg_offset: float = 0.8             # m from nose (center of gravity)
    cp_offset: float = 1.2             # m from nose (center of pressure)
    max_gimbal_angle: float = math.radians(5.0)  # rad

    @property
    def reference_area(self) -> float:
        """Cross-sectional area for drag calculation (m^2)."""
        return math.pi * (self.diameter / 2.0) ** 2

    @property
    def total_mass(self) -> float:
        """Initial total mass: dry + fuel (kg)."""
        return self.dry_mass + self.fuel_mass


@dataclass
class EnvironmentConfig:
    """Environmental parameters."""

    gravity: float = 9.81       # m/s^2
    air_density: float = 1.225  # kg/m^3 (sea level)


@dataclass
class SensorConfig:
    """Noise and bias parameters for simulated sensors."""

    # Accelerometer
    accel_noise_std: float = 0.5        # m/s^2
    accel_bias: float = 0.02            # m/s^2
    accel_sample_rate: float = 100.0    # Hz

    # Gyroscope
    gyro_noise_std: float = 0.01        # rad/s
    gyro_bias: float = 0.001            # rad/s
    gyro_sample_rate: float = 100.0     # Hz

    # Barometric altimeter
    altimeter_noise_std: float = 1.0    # m
    altimeter_bias: float = 0.5         # m
    altimeter_sample_rate: float = 50.0 # Hz

    # GPS (low-rate, moderate accuracy)
    gps_pos_noise_std: float = 2.0      # m
    gps_vel_noise_std: float = 0.3      # m/s
    gps_sample_rate: float = 10.0       # Hz


@dataclass
class KalmanConfig:
    """Tuning parameters for the Extended Kalman Filter."""

    # Process noise standard deviations
    process_noise_pos: float = 0.1      # m
    process_noise_vel: float = 1.0      # m/s
    process_noise_theta: float = 0.01   # rad
    process_noise_omega: float = 0.1    # rad/s

    # Initial state uncertainty (diagonal of P0)
    initial_pos_std: float = 5.0        # m
    initial_vel_std: float = 1.0        # m/s
    initial_theta_std: float = 0.1      # rad
    initial_omega_std: float = 0.05     # rad/s


@dataclass
class ControllerConfig:
    """PID controller gains and limits for pitch stabilization."""

    Kp: float = 10.0                    # proportional gain
    Ki: float = 0.5                     # integral gain
    Kd: float = 5.0                     # derivative gain

    target_theta: float = 0.0           # rad (desired pitch: 0 = vertical)

    output_min: float = -math.radians(5.0)  # rad (gimbal limit)
    output_max: float = math.radians(5.0)   # rad (gimbal limit)
    integral_limit: float = 5.0             # rad*s (anti-windup clamp)


@dataclass
class SimulationConfig:
    """Master configuration — aggregates all sub-configs.

    Usage:
        cfg = SimulationConfig()              # all defaults
        cfg = SimulationConfig(dt=0.005)      # override timestep
        cfg.rocket.max_thrust = 1500.0        # tweak after creation
    """

    dt: float = 0.01          # s  (simulation timestep, 100 Hz)
    t_end: float = 30.0       # s  (total duration)
    t_burn: float = 10.0      # s  (engine burn duration)

    rocket: RocketConfig = field(default_factory=RocketConfig)
    environment: EnvironmentConfig = field(default_factory=EnvironmentConfig)
    sensor: SensorConfig = field(default_factory=SensorConfig)
    kalman: KalmanConfig = field(default_factory=KalmanConfig)
    controller: ControllerConfig = field(default_factory=ControllerConfig)

    @property
    def n_steps(self) -> int:
        """Total number of integration steps."""
        return int(self.t_end / self.dt)
