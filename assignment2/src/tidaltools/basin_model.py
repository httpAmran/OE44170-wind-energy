"""0-D model of a one-way ebb-generation tidal range scheme (Appendix 2)."""

import numpy as np
from scipy.integrate import quad

from .harmonics import local_extrema

FILL, HOLD_HW, GEN, HOLD_LW = 1, 2, 3, 4
MODE_NAMES = {
    FILL: "Filling (sluicing)",
    HOLD_HW: "Holding (after HW)",
    GEN: "Generating (ebb)",
    HOLD_LW: "Holding (after generation)",
}


def basin_area(z, coeffs=(-264.55, -3835.98, -59920.6, 554761.9, 1.1e7)):
    """Basin area [m2] as a quartic in the basin water level z [m]."""
    return np.polyval(coeffs, z)


def tidal_energy_potential(range_m, area, rho=1025.0, g=9.81):
    """E = rho*g*A*R^2/2 [J], for a tide of range R over a constant area."""
    return rho * g * area * range_m**2 / 2


def tidal_energy_potential_variable_area(z_lo, z_hi, area_func, rho=1025.0, g=9.81):
    """Same, but integrated over a basin area that varies with level."""
    value, _ = quad(lambda z: area_func(z) * (z - z_lo), z_lo, z_hi)
    return rho * g * value


def ebb_ranges(t, y):
    """Every high water and the low water after it, as [t_hw, hw, lw, range]."""
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
    """Run the 0-D model against a tidal elevation series y(t_h).

    Cycles FILL -> HOLD_HW -> GEN -> HOLD_LW: the basin fills through the
    sluices and turbine passages (total open area a_fill), is held while the
    sea drops, generates between h_se and h_ee, then waits for the next flood.
    Returns the level, head, flow and power series as a dict.
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
    """Scale the energy over one simulated cycle to a full year [J]."""
    return year_factor * np.sum(power) * dt_s


def capacity_factor(aey_j, installed_power_w, hours_in_year=8760):
    """Capacity factor from AEY [J] and installed power [W]."""
    return aey_j / (installed_power_w * hours_in_year * 3600.0)
