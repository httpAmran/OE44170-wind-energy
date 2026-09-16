# OE44170 — Offshore Renewable Technologies 2026

Wind energy assignments for the course, shared by our group of 3.

## Layout

```
assignment1/            # this assignment's notebooks + PDF + checklist
  notebooks/
    part1_wind_resource.ipynb
    part2_energy_production.ipynb
    part3_turbine_technology.ipynb
assignment2/ .. 4/       # placeholders, filled in as released
src/windtools/            # shared, reusable Python code (import as `windtools`)
  weibull.py               # Weibull fitting (graphical / least-squares method)
  wind_profile.py           # log-law wind speed extrapolation
  power_curve.py             # load/interpolate turbine power curves, AEY, CF
  wake.py                     # Jensen wake model
  rotor_model.py                # Cp(beta, lambda) rotor curve, actuator disk theory
data/
  turbines/                # power curve CSVs (small, committed to git)
  wind/                     # NASA POWER downloads (gitignored, see its README)
```

**Why code lives outside the notebooks:** the notebooks are for plots and
narrative only. All the actual math (Weibull fit, wake model, etc.) is in
`src/windtools` as plain functions, imported into whichever notebook needs
them. This is reused across assignments 2-4, and — more importantly for a
3-person team — keeps notebook diffs small instead of every person's edits
colliding in one big JSON blob.

## One-time setup (each person)

```bash
git clone <repo-url>
cd OE44170-wind-energy
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .              # makes `import windtools` work everywhere
nbstripout --install          # strips notebook outputs from git diffs/commits
```

`nbstripout --install` sets up a git filter so committed notebooks never carry
cell outputs or execution counts — this is what keeps 3 people committing
notebooks from turning into constant merge conflicts. Run it once per clone.

## Git workflow

- `main` is always green — only merge finished, working assignment branches into it.
- For each assignment, branch off `main`: `assignment-1`, `assignment-2`, ...
- Within an assignment, each person branches off the *assignment* branch for
  their part, e.g. `amran/a1-part1`, `name2/a1-part2`, `name3/a1-part3`.
- Open a PR from your part-branch into the assignment branch when done (even
  just for each other to skim — catches silly mistakes early).
- Once all parts are in and the assignment notebooks run cleanly top-to-bottom,
  PR the assignment branch into `main`.

```
main ── assignment-1 ── amran/a1-part1
                     ── name2/a1-part2
                     ── name3/a1-part3
     ── assignment-2 ── ...
```

Avoid three people editing the *same* notebook file at once even on separate
branches — it's still JSON, and merges across branches touching the same
`.ipynb` are as painful as merges within one branch. Split by part/file
instead, like the layout above already does.

## Data

- `data/turbines/*.csv` — reference wind turbine power curves, committed (small, static).
- `data/wind/` — NASA POWER hourly wind speed downloads for your chosen site.
  Not committed (see `data/wind/README.md` for the exact parameters/site to
  re-download); every clone re-fetches its own copy.
