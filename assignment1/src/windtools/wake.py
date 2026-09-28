"""Jensen (Park) wake model, per Katic et al. (1986) as given in the
assignment: 1 - u2/u1 = (1 - sqrt(1 - Ct)) / (1 + k * x / r)^2
"""

import numpy as np


def wake_velocity_deficit(ct, x, r, k=0.038):
    """Fractional velocity deficit (1 - u2/u1) at downstream distance x."""
    return (1 - np.sqrt(1 - ct)) / (1 + k * x / r) ** 2


def downstream_speed(u1, ct, x, r, k=0.038):
    """Wake wind speed u2 at downstream distance x from an upstream turbine
    with thrust coefficient ct, inflow speed u1, and rotor radius r.
    """
    return u1 * (1 - wake_velocity_deficit(ct, x, r, k=k))


def array_efficiency(u_inflow, power_func, ct_func, rotor_radius, spacing, k=0.038, n_turbines=3):
    """Efficiency of n_turbines standing in a row with constant downstream
    spacing, each turbine seeing the (single, undisturbed) wake of the one
    directly upstream of it.

    Parameters
    ----------
    u_inflow : free-stream wind speed hitting the first turbine [m/s]
    power_func, ct_func : callables mapping wind speed -> power [kW] / Ct [-]
        (e.g. windtools.power_curve.power_at / ct_at bound to a power curve)
    rotor_radius : rotor radius [m]
    spacing : downstream distance between consecutive turbines [m]

    Returns
    -------
    efficiency, speeds, powers : array efficiency (sum of powers / (n *
        power of an undisturbed turbine)), and the per-turbine inflow
        speeds and powers.
    """
    speeds = [u_inflow]
    for _ in range(1, n_turbines):
        u_prev = speeds[-1]
        ct_prev = ct_func(u_prev)
        speeds.append(downstream_speed(u_prev, ct_prev, spacing, rotor_radius, k=k))

    powers = [float(power_func(u)) for u in speeds]
    power_free = float(power_func(u_inflow))
    efficiency = sum(powers) / (n_turbines * power_free)
    return efficiency, speeds, powers
