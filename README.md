# OE44170 — Offshore Renewable Technologies 2026

Wind energy assignments for the course, shared by our group of 3.

## Layout

```
assignment1/              # wind energy — fully self-contained, see below
  notebooks/
    part1_wind_resource.ipynb
    part2_energy_production.ipynb
    part3_turbine_technology.ipynb
  src/windtools/           # assignment 1's own copy of its shared code
  data/
    turbines/               # power curve CSVs (committed to git)
    wind/                    # NASA POWER downloads (not committed, see its README)
  Wind_energy_assignment_2026.pdf
assignment2/              # tidal energy — fully self-contained, see below
  notebooks/
    part1_tidal_resource.ipynb
    part2_stream_energy.ipynb
    part3_tidal_range.ipynb
  src/tidaltools/           # assignment 2's own copy of its shared code
  Tidal_range_Dataset_2026.csv
assignment3/              # electrical aspects
assignment4/              # wave energy
```

Every assignment folder is self-contained on purpose: each notebook only ever
reaches into its own `assignmentN/src/<name>tools` package and its own `data/`
files, never a shared top-level `src/` or `data/`. That means zipping up a
single `assignmentN/` folder (e.g. to submit it, or hand it to someone without
the rest of the repo) gives something that runs standalone. If assignment 3 or
4 need shared code, give them their own `src/<name>tools` copy the same way
rather than reusing another assignment's.
