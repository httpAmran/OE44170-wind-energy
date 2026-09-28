"""Rotor aerodynamics helpers for Part 3.

Two independent models are used in the assignment:
  1. Actuator disk / momentum theory (Q1: Cp from upstream/downstream speed).
  2. The empirical Cp(beta, lambda) rotor curve given in Appendix 2
     (Q2-Q4: tip speed ratio operating points, thrust at rated conditions).
"""

import numpy as np
from scipy.optimize import brentq

# --- Actuator disk / momentum theory -----------------------------------


def induction_factor_from_speeds(u1, u2):
    """Axial induction factor a from far-upstream (u1) and far-wake (u2)
    wind speeds, using u2 = u1 * (1 - 2a).
    """
    return (u1 - u2) / (2 * u1)


def cp_actuator_disk(a):
    """Power coefficient from axial induction factor: Cp = 4a(1-a)^2."""
    return 4 * a * (1 - a) ** 2


# --- Empirical Cp(beta, lambda) rotor curve (Appendix 2) ----------------


def lambda_i(beta, lam):
    """Intermediate variable lambda_i used in the empirical Cp expression."""
    return 1.0 / (1.0 / (lam - 0.02 * beta) - 0.003 / (beta**3 + 1))


def cp_empirical(beta, lam):
    """Empirical power coefficient Cp(beta, lambda) from Appendix 2.

    beta : collective pitch angle [degrees]
    lam  : tip speed ratio [-]
    """
    li = lambda_i(beta, lam)
    return 0.79 * (151 / li - 0.58 * beta - 0.002 * beta**2.14 - 13.2) * np.exp(-18.4 / li)


def tip_speed_ratio(omega_rpm, radius, wind_speed):
    """Tip speed ratio lambda = omega * R / U_wind, with omega given in rpm."""
    omega_rad_s = omega_rpm * 2 * np.pi / 60.0
    return omega_rad_s * radius / wind_speed


def aerodynamic_power(cp, rho_air, radius, wind_speed):
    """Aerodynamic power [W]: P = 0.5 * Cp * rho_air * pi * R^2 * U^3."""
    return 0.5 * cp * rho_air * np.pi * radius**2 * wind_speed**3


def axial_induction_from_cp(cp, branch="below_rated"):
    """Solve Cp = 4a(1-a)^2 for the axial induction factor a.

    Two solutions exist below the Betz limit; 'below_rated' returns the
    a < 1/3 branch (normal turbine operation), 'above_rated' the a > 1/3
    branch.
    """
    if branch == "below_rated":
        return brentq(lambda a: cp_actuator_disk(a) - cp, 0.0, 1.0 / 3.0)
    return brentq(lambda a: cp_actuator_disk(a) - cp, 1.0 / 3.0, 0.5)


def ct_from_induction(a):
    """Thrust coefficient from axial induction factor: Ct = 4a(1-a)."""
    return 4 * a * (1 - a)


def thrust_force(ct, rho_air, radius, wind_speed):
    """Rotor thrust force [N]: T = 0.5 * Ct * rho_air * pi * R^2 * U^2."""
    return 0.5 * ct * rho_air * np.pi * radius**2 * wind_speed**2
