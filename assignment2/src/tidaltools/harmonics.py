"""Harmonic superposition of tidal constituents (Part 1a, Appendix 1).

The tidal current is written as a sum of harmonic constituents:

    U(t) = sum_i U_A,i * cos(2*pi*t / T_A,i + phi_A,i)

and the beat between two constituents of slightly different period sets the
modulation period (e.g. the spring-neap cycle, from the M2-S2 beat).
"""

import numpy as np

KNOT = 0.514444  # m/s per knot


def superpose_constituents(t, constituents, phases=None):
    """Superpose harmonic constituents into a time series U(t).

    Parameters
    ----------
    t : array-like, time [h]
    constituents : dict of name -> (amplitude [m/s], period [h])
    phases : optional dict of name -> phase [rad], default 0 for all

    Returns
    -------
    U : ndarray, superposed signal at each t
    """
    t = np.asarray(t, dtype=float)
    U = np.zeros_like(t)
    for name, (amp, period) in constituents.items():
        phi = 0.0 if phases is None else phases.get(name, 0.0)
        U += amp * np.cos(2 * np.pi * t / period + phi)
    return U


def beat_period(period_a, period_b):
    """Beat (modulation) period between two constituents of periods
    period_a, period_b, e.g. the M2-S2 spring-neap beat.
    """
    return 1.0 / (1.0 / period_b - 1.0 / period_a)


def local_extrema(x, kind="max"):
    """Indices of strict interior local extrema of a 1-D array.

    kind="max" finds local maxima, kind="min" finds local minima. Used to
    pick out envelope peaks of a current-speed series, or high/low waters
    of a tidal elevation series.
    """
    x = np.asarray(x, dtype=float)
    if kind == "max":
        is_ext = (x[1:-1] >= x[:-2]) & (x[1:-1] > x[2:])
    elif kind == "min":
        is_ext = (x[1:-1] <= x[:-2]) & (x[1:-1] < x[2:])
    else:
        raise ValueError("kind must be 'max' or 'min'")
    return np.where(is_ext)[0] + 1
