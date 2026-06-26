# Water Feature MVP Slice

## Farmer job

The first useful farmer/landowner job is:

> Show me where the wet places, ditches, streams, runoff paths, or water-holding
> opportunities are, then help me choose one useful water or habitat
> intervention to turn into a JobDone work package.

This is deliberately farmer-facing. It should start with a plain-language map
and a small set of candidate places, not with grant machinery.

## Local evidence now available

Raw Dewlish Estate Farm USB data is copied to ignored local storage:

```text
local/raw/dewlish-usb-2026-06-26/
```

Derived ignored helper files created so far:

```text
local/derived/field-kml-index.json
local/derived/pdf-text/
```

The copied data includes:

- field KML exports inside `Field_*.zip`
- ISO11783 / AGCO task data inside field and implement exports
- soil analysis PDFs and spreadsheets
- soil management plans
- NVZ and nutrient management reports
- maps and analysis reports

## First local clues

These are candidate investigation leads, not recommendations yet.

### Name-based water clues

- `River`
- `River Meadow`
- `Lower Flippings`
- `Lower New Close`
- `Malthouse Mead`
- `Rookery Mead Meadow`
- `Cowleaze`

### Risk-based water/runoff clues from the soil management plan

Fields with explicit high runoff or steep/high erosion signals should be checked
for runoff interception, leaky dams, swales, buffer strips, tree belts, or
similar work:

- `Kitehill` - very high erosion risk, high runoff risk, steep slope.
- `Higher Kitehills` - very high erosion risk, high runoff risk, steep slope.
- `Rookery Mead Meadow` - high runoff risk, steep slope.
- `River` - high erosion risk, moderate runoff risk.
- `Road` - high erosion risk, moderate runoff risk.
- `Puddle Town Down` - high erosion risk, moderate runoff risk.
- `Fat Ox` - high erosion risk, moderate runoff risk.
- `Chebbard Drive` - high erosion risk, moderate runoff risk.
- `Bulls Ground` - high erosion risk, moderate runoff risk.
- `Chalky Ground` - high erosion risk, moderate runoff risk.
- `Cowleaze` - high erosion risk, moderate runoff risk.
- `Lower Flippings` - high erosion risk, moderate runoff risk.

## External data layers to add

For a useful first pass, combine the farm data with:

- open river / watercourse vectors
- digital terrain model / LiDAR elevation
- slope and flow accumulation derived from elevation
- flood / surface water risk layers
- soil type and drainage class where available

## PyLUSAT decision

PyLUSAT is useful prior art for the suitability-analysis layer. Do not fork it
yet.

Use it as a reference for the boring geospatial operations:

- distance to lines or points
- reclassification
- zonal statistics
- raster/vector joins
- weighted suitability scoring
- analytic hierarchy process

The RegenOS value is not a generic suitability library. The value is the
farmer-facing restoration workflow:

1. identify candidate wet/water places
2. explain why they look interesting
3. let the farmer choose one
4. create a practical intervention plan
5. export a JobDone work package
6. capture evidence

Fork PyLUSAT only if a real integration test shows its API, dependency shape, or
maintenance state blocks the RegenOS workflow.

## First implementation slice

Build a local, reproducible command that:

1. reads field KMLs from the ignored raw folder
2. extracts field names, geometry bounds, and centroids
3. extracts field risk clues from the soil management plan text
4. ranks fields by simple water-interest heuristics
5. writes an ignored HTML/GeoJSON report for Peter to inspect

The report should label every candidate as `clue`, not `recommendation`.
