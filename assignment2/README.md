# Assignment 2 — Tidal Energy

Full task text: [Tidal_energy_assignment_2026.pdf](Tidal_energy_assignment_2026.pdf) (not committed — see Brightspace)

Notebooks live in [`notebooks/`](notebooks/) and import shared logic from the
`tidaltools` package in [`src/tidaltools`](src/tidaltools) — kept local to this
folder (not the repo's top-level `src/`) so this whole `assignment2/` directory
is self-contained: zip it up on its own and the notebooks still run, no other
part of the repo required. Site data: **Group 21** (Appendix 1, wraps to row 1,
SN167BV). Tidal range input data: [`Tidal_range_Dataset_2026.csv`](Tidal_range_Dataset_2026.csv).

## Checklist

### Part 1a — Environmental Data and Tidal Resource [20 pts] — [`part1_tidal_resource.ipynb`](notebooks/part1_tidal_resource.ipynb)
- [ ] Harmonic superposition (M2, S2, K2) of the year-long hourly current velocity [—]
- [ ] Plot of current velocity vs. time for 30 days, showing the neap and spring cycle [20]

### Part 1b — Tidal Stream Energy Production [25 pts] — [`part2_stream_energy.ipynb`](notebooks/part2_stream_energy.ipynb)
- [ ] Plot of generated power vs. time for 31 days (bi-directional turbine) [15]
- [ ] Annual mean power and max power produced [5]
- [ ] Annual energy yield (AEY) and capacity factor (CF) [5]

### Part 2 — Operation of a Tidal Range Power Plant [55 pts] — [`part3_tidal_range.ipynb`](notebooks/part3_tidal_range.ipynb)
- [ ] Energy potential of the basin during a spring and a neap tide [10]
- [ ] Plot of basin water level and head difference over the 14-day spring-neap cycle [10]
- [ ] Plot of tidal elevation and basin water level for the first 50 hours, with operating modes [10]
- [ ] Plot of total hydraulic power and total power produced, first 50 hours [10]
- [ ] Plot of total flow rates, first 50 hours [10]
- [ ] Annual energy yield (AEY) and capacity factor (CF) [5]

`tidal_energy_assignment.ipynb` is the original single-notebook draft, kept for
reference — the checklist above is implemented in `notebooks/`.
