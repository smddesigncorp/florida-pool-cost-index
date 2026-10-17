# Florida Pool Cost Index

Static site showing Florida pool and screen enclosure costs by county: official permit aggregates, builder-contributed quotes (anonymized), and published estimates, each labeled by source.

- `data.json` – all data (county-level aggregates and summary statistics of anonymized builder quotes only; no individual quotes, addresses, or personal names).
- `build.py` – generates the static site into `site/` (Python 3 standard library only).
- `site/` – the generated site (committed, so it can be served as-is).

## Build

    python3 build.py

## Deploy (Render static site)

- Build command: `python3 build.py` (or leave blank and serve the committed `site/`)
- Publish directory: `site`

Not legal, financial, or contracting advice.
