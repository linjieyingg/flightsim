"""Smoke tests for Phase 1 foundation."""

import math

import numpy as np

from sim.config import SimulationConfig, RocketConfig
from sim.state import RocketState
from sim.result import SimulationResult, FlightRecord
from sim.utils import clamp, wrap_angle, body_to_world


def test_config_defaults():
    cfg = SimulationConfig()
    assert cfg.dt == 0.01
    assert cfg.rocket.dry_mass == 50.0
    assert cfg.rocket.total_mass == 80.0
    assert cfg.n_steps == 3000


def test_config_override():
    cfg = SimulationConfig(dt=0.005, rocket=RocketConfig(dry_mass=100.0))
    assert cfg.dt == 0.005
    assert cfg.rocket.dry_mass == 100.0
    assert cfg.rocket.total_mass == 130.0  # 100 dry + 30 fuel


def test_state_array_roundtrip():
    s = RocketState(x=1, y=2, vx=3, vy=4, theta=0.1, omega=0.2, mass=80)
    arr = s.to_array()
    assert arr.shape == (7,)
    s2 = RocketState.from_array(arr)
    assert abs(s2.x - 1.0) < 1e-12
    assert abs(s2.y - 2.0) < 1e-12
    assert abs(s2.theta - 0.1) < 1e-12
    assert abs(s2.mass - 80.0) < 1e-12


def test_simulation_result():
    result = SimulationResult()
    for i in range(10):
        state = RocketState(y=float(i))
        record = FlightRecord(time=i * 0.01, state=state)
        result.append(record)
    assert len(result.records) == 10
    np.testing.assert_almost_equal(result.times[-1], 0.09)
    assert result.y[5] == 5.0


def test_clamp():
    assert clamp(5.0, 0.0, 10.0) == 5.0
    assert clamp(-1.0, 0.0, 10.0) == 0.0
    assert clamp(15.0, 0.0, 10.0) == 10.0


def test_wrap_angle():
    assert abs(wrap_angle(0.0)) < 1e-12
    assert abs(wrap_angle(2 * math.pi)) < 1e-12
    assert abs(wrap_angle(math.pi + 0.1) - (-math.pi + 0.1)) < 1e-12
    assert abs(wrap_angle(-math.pi - 0.1) - (math.pi - 0.1)) < 1e-12


def test_body_to_world_vertical():
    """theta=0: rocket pointing up. Thrust along body x (nose) -> world +y."""
    thrust_body = np.array([1.0, 0.0])
    thrust_world = body_to_world(thrust_body, theta=0.0)
    assert abs(thrust_world[0]) < 1e-12        # no horizontal component
    assert abs(thrust_world[1] - 1.0) < 1e-12  # all vertical (up)
