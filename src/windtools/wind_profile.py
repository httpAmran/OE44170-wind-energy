"""Vertical extrapolation of wind speed using the logarithmic wind profile
(neutral atmospheric stability, i.e. atmospheric stability effects neglected).
"""

import numpy as np


def roughness_length(u1, z1, u2, z2):
    """Estimate roughness length z0 from two known wind speeds at two
    heights, using the log law:  u(z) = (u* / kappa) * ln(z / z0)
    """
    return np.exp((u1 * np.log(z2) - u2 * np.log(z1)) / (u1 - u2))


def extrapolate_log_law(u_ref, z_ref, z_target, z0):
    """Extrapolate a reference wind speed u_ref measured at height z_ref
    to a target height z_target, given roughness length z0.
    """
    return u_ref * np.log(z_target / z0) / np.log(z_ref / z0)
