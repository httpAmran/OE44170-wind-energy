"""Loading and interpolating manufacturer power curves (Part 2)."""

import numpy as np
import pandas as pd


def load_power_curve(csv_path):
    """Load a turbine power curve CSV and return a clean DataFrame.

    Handles the trailing empty columns present in some of the source files
    and strips whitespace from column names.
    """
    df = pd.read_csv(csv_path)
    df.columns = [c.strip() for c in df.columns]
    df = df.loc[:, ~df.columns.str.startswith("Unnamed")]
    df = df.dropna(how="all")
    return df.sort_values(df.columns[0]).reset_index(drop=True)


def power_at(power_curve, wind_speed, cut_in=None, cut_out=None):
    """Interpolate rated power [kW] at the given wind speed(s) [m/s].

    Wind speeds outside [cut_in, cut_out] (if provided) return 0.
    """
    v_col, p_col = power_curve.columns[0], power_curve.columns[1]
    wind_speed = np.asarray(wind_speed, dtype=float)
    power = np.interp(wind_speed, power_curve[v_col], power_curve[p_col], left=0.0, right=0.0)
    if cut_in is not None:
        power = np.where(wind_speed < cut_in, 0.0, power)
    if cut_out is not None:
        power = np.where(wind_speed > cut_out, 0.0, power)
    return power


def ct_at(power_curve, wind_speed):
    """Interpolate thrust coefficient Ct [-] at the given wind speed(s).

    Requires the power curve to have a 'Ct [-]' column (not all turbines do).
    """
    if "Ct [-]" not in power_curve.columns:
        raise ValueError("This power curve has no 'Ct [-]' column")
    v_col = power_curve.columns[0]
    wind_speed = np.asarray(wind_speed, dtype=float)
    return np.interp(wind_speed, power_curve[v_col], power_curve["Ct [-]"])


def annual_energy_yield(power_curve, wind_speed_series, hours_per_sample=1.0, cut_in=None, cut_out=None):
    """Annual Energy Yield [MWh] from a time series of wind speeds.

    Parameters
    ----------
    wind_speed_series : array-like of hourly (or other constant-step) wind
        speeds for one year at hub height.
    hours_per_sample : number of hours represented by each sample
        (1.0 for hourly data).
    """
    power_kw = power_at(power_curve, wind_speed_series, cut_in=cut_in, cut_out=cut_out)
    energy_kwh = np.sum(power_kw * hours_per_sample)
    return energy_kwh / 1000.0  # MWh


def capacity_factor(aey_mwh, rated_power_kw, hours_in_year=8760):
    """Capacity factor [-] given AEY [MWh] and rated power [kW]."""
    max_energy_mwh = (rated_power_kw / 1000.0) * hours_in_year
    return aey_mwh / max_energy_mwh
