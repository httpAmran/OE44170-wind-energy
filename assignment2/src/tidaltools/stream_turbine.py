"""Bi-directional hydrokinetic turbine."""

import numpy as np


def rated_speed(p_rated, rho, area, eta):
    """Speed [m/s] at which the cubic power law reaches p_rated."""
    return (p_rated / (0.5 * rho * area * eta)) ** (1 / 3)


def bidirectional_power(u, rho, area, eta, p_rated, u_cut_in, u_cut_out):
    """Electrical power [W] for current speed(s) u; only |u| matters."""
    u = np.asarray(u, dtype=float)
    speed = np.abs(u)
    power = np.minimum(0.5 * rho * area * eta * speed**3, p_rated)
    return np.where((speed < u_cut_in) | (speed > u_cut_out), 0.0, power)


def annual_energy_yield(power, dt=1.0):
    """Energy [Wh] from a power series [W] sampled every dt hours."""
    return np.sum(power) * dt


def capacity_factor(aey, rated_power, hours_in_year=8760):
    """Capacity factor from energy yield [Wh] and rated power [W]."""
    return aey / (rated_power * hours_in_year)
