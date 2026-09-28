"""0-D model of a one-way ebb-generation tidal range power plant (Part 2,
Appendix 2), with a variable basin area A(Z).

Mass balance, discretised with a backward difference scheme:

    Z[i+1] = Z[i] + Q[i] / A(Z[i]) * dt

Operating modes cycle FILL -> HOLD_HW -> GEN -> HOLD_LW -> FILL:
  FILL    : sea rising above the held basin level; sluices + turbine
            passages open, water flows in via the orifice equation.
  HOLD_HW : basin held near high water while the sea falls, until H >= Hse.
  GEN     : turbines generate while H = Z - Y is between Hee and Hse.
  HOLD_LW : basin held near low water (head too small to generate) until
            the sea rises back above the basin (H < 0).
"""

import numpy as np
from scipy.integrate import quad

FILL, HOLD_HW, GEN, HOLD_LW = 1, 2, 3, 4
MODE_NAMES = {
    FILL: "Filling (sluicing)",
    HOLD_HW: "Holding (after HW)",
    GEN: "Generating (ebb)",
    HOLD_LW: "Holding (after generation)",
}


def basin_area(z, coeffs=(-264.55, -3835.98, -59920.6, 554761.9, 1.1e7)):
    """Basin area A(Z) [m^2] as a quartic polynomial in water level Z [m]."""
    return np.polyval(coeffs, z)


def tidal_energy_potential(range_m, area, rho=1025.0, g=9.81):
    """Maximum energy [J] available from one tide of range `range_m` [m]
    trapped over a constant basin area [m^2]: E = rho * g * A * R^2 / 2.
    """
    return rho * g * area * range_m**2 / 2


def tidal_energy_potential_variable_area(z_lo, z_hi, area_func, rho=1025.0, g=9.81):
    """Energy [J] released lowering the basin from z_hi to z_lo, accounting
    for the basin area changing with level: E = rho*g* int_(z_lo)^(z_hi) A(z)*(z - z_lo) dz.
    """
    value, _ = quad(lambda z: area_func(z) * (z - z_lo), z_lo, z_hi)
    return rho * g * value


def ebb_ranges(t, y):
    """Tidal range of every ebb (high water -> following low water).

    Returns an (n, 4) array of columns [t_hw, hw_level, lw_level, range].
    """
    from .harmonics import local_extrema

    i_hw = local_extrema(y, kind="max")
    i_lw = local_extrema(y, kind="min")

    ranges = []
    for i in i_hw:
        nxt = i_lw[i_lw > i]
        if len(nxt):
            ranges.append((t[i], y[i], y[nxt[0]], y[i] - y[nxt[0]]))
    return np.array(ranges)


def simulate_one_way_ebb(t_h, y, area_func, n_turb, q_turb, eta_t, a_fill,
                          h_se, h_ee, cd=1.0, rho=1025.0, g=9.81):
    """Simulate a one-way ebb-generation scheme against a tidal elevation
    series y(t) [m about MSL], sampled at constant intervals t_h [h].

    Parameters
    ----------
    area_func : callable, basin area A(Z) [m^2]
    n_turb, q_turb : number of turbines, and (constant) flow rate per
        turbine while generating [m^3/s]
    eta_t : fixed turbine efficiency [-]
    a_fill : total open area (sluices + turbine passages) while filling [m^2]
    h_se, h_ee : head [m] at which generation starts / stops
    cd : discharge coefficient for the filling orifice equation

    Returns
    -------
    dict with keys Z, H, Q, Q_sl, Q_tb, P_hyd, P_el, mode (all length-n
    arrays); Z[0] is initialised to y[0].
    """
    t_h = np.asarray(t_h, dtype=float)
    y = np.asarray(y, dtype=float)
    dt_s = (t_h[1] - t_h[0]) * 3600.0

    n = len(y)
    Z = np.zeros(n)
    H = np.zeros(n)
    Q = np.zeros(n)
    Q_sl = np.zeros(n)
    Q_tb = np.zeros(n)
    P_hyd = np.zeros(n)
    P_el = np.zeros(n)
    mode = np.zeros(n, dtype=int)

    Z[0] = y[0]
    m = HOLD_HW

    for i in range(n):
        H[i] = Z[i] - y[i]
        sea_falling = i > 0 and y[i] < y[i - 1]

        if m == FILL and H[i] >= 0 and sea_falling:
            m = HOLD_HW
        elif m == HOLD_HW and H[i] >= h_se:
            m = GEN
        elif m == GEN and H[i] < h_ee:
            m = HOLD_LW
        elif m == HOLD_LW and H[i] < 0:
            m = FILL
        mode[i] = m

        if m == FILL and H[i] < 0:
            Q_sl[i] = cd * a_fill * np.sqrt(2 * g * -H[i])
        elif m == GEN:
            Q_tb[i] = n_turb * q_turb
            P_hyd[i] = rho * g * H[i] * Q_tb[i]
            P_el[i] = eta_t * P_hyd[i]
        Q[i] = Q_sl[i] - Q_tb[i]

        if i < n - 1:
            Z[i + 1] = Z[i] + Q[i] / area_func(Z[i]) * dt_s

    return {"Z": Z, "H": H, "Q": Q, "Q_sl": Q_sl, "Q_tb": Q_tb,
            "P_hyd": P_hyd, "P_el": P_el, "mode": mode}


def annual_energy_yield(power, dt_s, year_factor):
    """Scale energy produced over the simulated period [W, s] to an annual
    energy yield [J], using `year_factor` (number of such periods per year).
    """
    return year_factor * np.sum(power) * dt_s


def capacity_factor(aey_j, installed_power_w, hours_in_year=8760):
    """Capacity factor [-] given AEY [J] and installed power [W]."""
    return aey_j / (installed_power_w * hours_in_year * 3600.0)
