"""Weibull distribution fitting via the graphical (least-squares) method.

Implements the method described in Appendix 1 of the assignment: linearize
the Weibull CDF with a double-log transform, fit a straight line via least
squares, and recover the shape (k) and scale (c) parameters from the slope
and intercept.
"""

import numpy as np


def fit_weibull_lsq(wind_speeds):
    """Estimate Weibull shape (k) and scale (c) parameters using the
    graphical method of least squares (Appendix 1): sort the data, assign
    each point an empirical CDF via the Weibull plotting position
    F_i = i / (n + 1), then fit a straight line to the double-log-transformed
    data.

    Returns
    -------
    k, c, r2, x, y : shape factor, scale factor, coefficient of
        determination, and the transformed (x, y) points used in the fit
        (useful for plotting the linear regression).
    """
    v = np.sort(np.asarray(wind_speeds, dtype=float))
    n = len(v)
    i = np.arange(1, n + 1)
    F = i / (n + 1)

    x = np.log(v)
    y = np.log(-np.log(1 - F))

    a = (n * np.sum(x * y) - np.sum(x) * np.sum(y)) / (n * np.sum(x**2) - np.sum(x) ** 2)
    b = (np.sum(y) * np.sum(x**2) - np.sum(x) * np.sum(x * y)) / (n * np.sum(x**2) - np.sum(x) ** 2)

    k = a
    c = np.exp(-b / a)

    y_pred = a * x + b
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot

    return k, c, r2, x, y


def weibull_pdf(v, k, c):
    """Weibull probability density function."""
    v = np.asarray(v, dtype=float)
    return (k / c) * (v / c) ** (k - 1) * np.exp(-((v / c) ** k))


def rmse_pdf(wind_speeds, k, c, bin_width=1.0):
    """RMSE between the normalized histogram of wind_speeds and the fitted
    Weibull PDF, evaluated at bin centers.
    """
    wind_speeds = np.asarray(wind_speeds)
    edges = np.arange(0, wind_speeds.max() + bin_width, bin_width)
    density, edges = np.histogram(wind_speeds, bins=edges, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    predicted = weibull_pdf(centers, k, c)
    return np.sqrt(np.mean((density - predicted) ** 2))
