# Wind speed data

Not committed to git (see `.gitignore`) — NASA POWER exports can be re-downloaded
by anyone with the site coordinates below, and hourly-resolution yearly data adds
up quickly.

## Site

- **Location:** TODO (lat, lon)
- **Source:** [NASA POWER](https://power.larc.nasa.gov/), hourly data, year 2025
- **Parameters used:** wind speed at 10 m (`WS10M`) and 50 m (`WS50M`)

## How to re-download

1. Go to https://power.larc.nasa.gov/data-access-viewer/
2. Select the site coordinates above, hourly temporal resolution, 2025.
3. Request parameters `WS10M` and `WS50M`.
4. Save the CSV(s) into this folder.

If you place a raw download here, keep it under `data/wind/raw/` — that
sub-path is already gitignored.
