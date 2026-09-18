# Wind speed data

Not committed to git (see `.gitignore`) — NASA POWER exports can be re-downloaded
by anyone with the site coordinates below, and hourly-resolution yearly data adds
up quickly.

## Site

- **Location:** 54.091 N, 3.741 W (Irish Sea, off the Cumbria coast, UK)
- **Source:** [NASA POWER](https://power.larc.nasa.gov/), hourly data, year 2025
- **Parameters used:** wind speed at 10 m (`WS10M`) and 50 m (`WS50M`)
- **Expected filename:** `POWER_Point_Hourly_20250101_20251231_054d09N_003d74W_LST.csv`
  (NASA POWER's default naming — the notebooks look for exactly this)

## How to re-download

1. Go to https://power.larc.nasa.gov/data-access-viewer/
2. Select the site coordinates above, hourly temporal resolution, 2025.
3. Request parameters `WS10M` and `WS50M`.
4. Save the CSV directly into this folder (`data/wind/`) — everything here
   except this README is gitignored, so it won't get committed.
