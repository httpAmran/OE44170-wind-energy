# Assignment 1 — Wind Resource, Energy Production & Turbine Technology

Full task text: [Wind_energy_assignment_2026.pdf](Wind_energy_assignment_2026.pdf)

Notebooks live in [`notebooks/`](notebooks/) and import shared logic from the
`windtools` package in [`/src/windtools`](../src/windtools) — see the top-level
[README](../README.md) for setup.

## Checklist

### Part 1 — Wind Resource [40 pts] — [`part1_wind_resource.ipynb`](notebooks/part1_wind_resource.ipynb)
- [ ] Normalized histogram (1 m/s bins), annual average U, std. dev. [10]
- [ ] Weibull k, c via graphical least-squares method, report R² [20]
- [ ] Weibull PDF overlaid on histogram + RMSE [5]
- [ ] Written reflection on the site's results [5]

### Part 2 — Wind Energy Production [40 pts] — [`part2_energy_production.ipynb`](notebooks/part2_energy_production.ipynb)
- [ ] Power curves for 2 chosen turbines [5]
- [ ] Hub-height extrapolation via log law (roughness length from 10 m & 50 m data) [10]
- [ ] AEY and capacity factor for both turbines [10]
- [ ] Jensen wake model: 3-turbine row, 6D spacing, k = 0.038, array efficiency [10]
- [ ] Turbine recommendation + justification [5]

### Part 3 — Wind Turbine Technology [20 pts] — [`part3_turbine_technology.ipynb`](notebooks/part3_turbine_technology.ipynb)
- [ ] Cp from u1 = 10, u2 = 7 m/s [5]
- [ ] Tip speed ratio & Cp at U = 15 m/s, 7.8 rpm [5]
- [ ] Expected Cp at U = 9 m/s, 5.4 rpm [5]
- [ ] Thrust force at rated conditions [5]
