#!/usr/bin/env python3
"""Entry point for the rocket flight simulation."""

from sim.config import SimulationConfig
from sim.state import RocketState


def main() -> None:
    cfg = SimulationConfig()
    initial_state = RocketState(mass=cfg.rocket.total_mass)

    print("=== Rocket Flight Simulation ===")
    print(f"Rocket: {cfg.rocket.dry_mass} kg dry + {cfg.rocket.fuel_mass} kg fuel "
          f"= {cfg.rocket.total_mass} kg total")
    print(f"Thrust: {cfg.rocket.max_thrust} N | Isp: {cfg.rocket.Isp} s")
    print(f"T/W ratio: {cfg.rocket.max_thrust / (cfg.rocket.total_mass * cfg.environment.gravity):.2f}")
    print(f"Burn time: {cfg.t_burn} s")
    print(f"Simulation: {cfg.t_end} s at dt={cfg.dt} s ({cfg.n_steps} steps)")
    print(f"Initial state: {initial_state}")


if __name__ == "__main__":
    main()
