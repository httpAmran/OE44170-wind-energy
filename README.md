# OE44170 — Offshore Renewable Technologies 2026

Wind energy assignments for the course, shared by our group of 3.

## Layout

```
assignment1/            # this assignment's notebooks + PDF + checklist
  notebooks/
    part1_wind_resource.ipynb
    part2_energy_production.ipynb
    part3_turbine_technology.ipynb
assignment2/              # tidal energy
assignment3/              # electrical aspects
assignment4/              # wave energy
src/windtools/            # shared Python code used across notebooks (weibull fit,
                           # log-law wind profile, power curves, Jensen wake model,
                           # rotor Cp/lambda curves)
data/
  turbines/                # power curve CSVs (committed to git)
  wind/                     # NASA POWER downloads (not committed, see its README)
```

The math (Weibull fit, wake model, etc.) lives in `src/windtools` instead of being
copy-pasted into every notebook, so it can be reused across assignments 2-4.

