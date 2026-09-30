"""Harmonic superposition of tidal constituents."""

import numpy as np

KNOT = 0.514444  # m/s per knot


def superpose_constituents(t, constituents, phases=None):
    """U(t) = sum of amp * cos(2*pi*t/period + phase) over the constituents.

    t in hours, constituents as {name: (amplitude, period [h])}.
    """
    t = np.asarray(t, dtype=float)
    U = np.zeros_like(t)
    for name, (amp, period) in constituents.items():
        phi = 0.0 if phases is None else phases.get(name, 0.0)
        U += amp * np.cos(2 * np.pi * t / period + phi)
    return U


def beat_period(period_a, period_b):
    """Beat period between two constituents, e.g. M2-S2 gives spring-neap."""
    return 1.0 / (1.0 / period_b - 1.0 / period_a)


def local_extrema(x, kind="max"):
    """Indices of the interior local maxima ("max") or minima ("min") of x."""
    x = np.asarray(x, dtype=float)
    if kind == "max":
        is_ext = (x[1:-1] >= x[:-2]) & (x[1:-1] > x[2:])
    elif kind == "min":
        is_ext = (x[1:-1] <= x[:-2]) & (x[1:-1] < x[2:])
    else:
        raise ValueError("kind must be 'max' or 'min'")
    return np.where(is_ext)[0] + 1
