# inaturalist-clumper

[![GitHub repo](https://img.shields.io/badge/github-repo-green)](https://github.com/simonw/inaturalist-clumper)
[![PyPI](https://img.shields.io/pypi/v/inaturalist-clumper.svg)](https://pypi.org/project/inaturalist-clumper/)
[![Changelog](https://img.shields.io/github/v/release/simonw/inaturalist-clumper?include_prereleases&label=changelog)](https://inaturalist-clumper.datasette.io/en/stable/changelog.html)
[![Tests](https://github.com/simonw/inaturalist-clumper/workflows/Test/badge.svg)](https://github.com/simonw/inaturalist-clumper/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/inaturalist-clumper/blob/main/LICENSE)

Group iNaturalist sightings into clumps, represented as JSON.

Given one or more iNaturalist user logins, this CLI fetches every public observation those users have recorded and groups sightings that happened **within ~5 km and ~3 hours of each other** into "clumps" — useful for reconstructing a single hike, birding session, or tide-pool visit as one record.

See [simonw/inaturalist-clumps/blob/main/clumps.json](https://github.com/simonw/inaturalist-clumps/blob/main/clumps.json) for example output from this tool.

The output JSON file records, for every clump:

- start/end timestamps, duration, centroid, bounding box, span
- a species roll-up
- a `location` block: the mode of the observations' `place_guess` plus the most-specific iNaturalist place that every observation in the clump falls inside (with a `breadcrumb` of ancestor place IDs)
- per-observation: timestamp, latitude/longitude, identified taxon, user-typed `place_guess`, iNat `place_ids`, and photo URLs (thumbnail / large / original)

A top-level `places` dictionary caches the iNat place metadata (`name`, `display_name`, `admin_level`, `ancestor_ids`) for every ID that appears in a clump's `breadcrumb`, so the file is self-contained. Incremental runs reuse this cache and only fetch newly-referenced places.

## Install

```bash
pip install inaturalist-clumper
```
Or:
```bash
uv tool install inaturalist-clumper
```

## Usage

```bash
inaturalist-clumper simonw --output clumps.json
```
You can pass more than one iNaturalist username to gather sightings from multiple users accounts.

Options:

- `USERNAME ...` — **required**  
  One or more iNaturalist user logins to fetch.
- `--output` — default: `clumps.json`  
  Output JSON path. Used as the basis for incremental runs if it exists.
- `--distance-km` — default: `5.0`  
  Spatial threshold for linking two observations into the same clump.
- `--hours` — default: `3.0`  
  Temporal threshold for linking two observations into the same clump.
- `--full-refresh` — default: off  
  Ignore any existing observations in the output file and re-fetch fully.

### Incremental runs

A second invocation against the same `--output` file reads the existing data and asks the iNaturalist API for any observations that have been created or edited since the previous run's `generated_at` timestamp (using the `updated_since` parameter). Edited records overwrite the cached copy on merge, so corrected taxa, new photos, or fixed coordinates flow back in. The full set is then re-clumped and the file rewritten — so a new sighting that bridges two previous clumps will merge them.

Use `--full-refresh` to ignore the existing file and start over.

## Development

Clone the repo and then:
```bash
uv run pytest
```
To run the development version:
```bash
uv run inaturalist-clumper --help
```
