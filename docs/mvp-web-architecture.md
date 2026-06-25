# MVP web architecture

RegenOS should not require farmers or land managers to learn QGIS.

QGIS is powerful, but it is the wrong primary interface for this audience. The farmer-facing product should be a web map with simple prompts, sensible defaults, and domain-specific workflows.

## Product principle

```text
Google Maps simplicity
+
restoration intelligence
+
funding/evidence workflow
+
JobDone execution
```

Not:

```text
QGIS with nicer buttons
```

## Target MVP workflow

1. User opens RegenOS in a browser.
2. User searches by postcode, farm name, grid reference, or map location.
3. User draws or imports field boundaries.
4. User toggles useful layers.
5. User marks obvious landscape features:
   - wet corner
   - ditch
   - flow path
   - existing pond
   - awkward field edge
   - unproductive patch
6. RegenOS suggests possible interventions:
   - pond
   - check dam / leaky dam
   - tree planting
   - hedge restoration
   - riparian fencing
   - wetland/scrape
7. User accepts, rejects, or edits suggestions.
8. RegenOS generates:
   - project summary
   - mapped intervention plan
   - rough task list
   - evidence checklist
   - JobDone work package export

## MVP architecture

```text
Browser web app
  - map interface
  - drawing tools
  - layer toggles
  - project/intervention forms
  - import wizard
        |
        v
API server
  - projects
  - farms/fields
  - interventions
  - funding options
  - work package generation
  - evidence requirements
        |
        v
Data services
  - Postgres/PostGIS for core and spatial data
  - object storage for uploaded files/photos
  - template files for interventions and funding rules
        |
        v
Geo processing
  - boundary import/conversion
  - simple suitability scoring
  - layer intersection checks
  - later raster/hydrology tools
        |
        v
JobDone integration
  - export work package
  - import completion/evidence status later
```

## Frontend options

### Leaflet

Good for the first version.

Pros:

- simple
- mature
- easy drawing plugins
- easy to build quickly
- good enough for field boundaries and intervention markers

Cons:

- less modern vector styling
- can become clunky with lots of large layers

### MapLibre GL

Better long-term if RegenOS needs slick vector tiles and richer map styling.

Pros:

- modern vector maps
- smoother large datasets
- better styling system

Cons:

- steeper learning curve
- slightly more moving parts

### Recommendation

Start with Leaflet unless there is already strong MapLibre experience in the codebase.

The MVP is about workflow, not beautiful cartography.

## Backend options

The boring, robust choice:

- Postgres/PostGIS
- simple API server
- object storage for files
- YAML templates in git
- Python geospatial worker for imports/suitability experiments

Do not start with a complex microservice architecture.

## Data model for MVP

Minimum entities:

- user
- organisation
- farm/holding
- field/parcel
- spatial feature
- intervention proposal
- funding candidate
- task/work package
- evidence requirement
- evidence item

## Suitability engine MVP

Do not try to solve hydrology properly on day one.

Start with transparent rules:

- field boundary intersects flood-prone area
- low slope / low lying area
- near ditch or watercourse
- poor productivity or wet patch marked by farmer
- not obviously excluded by protected layer
- accessible by machinery

Output should be a suggestion, not an instruction.

Example:

> This corner may suit a pond because it is low lying, close to a ditch, and has been marked as wet/unproductive.

## Role of QGIS

QGIS can still be useful for:

- developer exploration
- adviser power users
- debugging layers
- preparing datasets
- complex one-off analysis

But it should not be part of the standard farmer workflow.

## Build order

1. Web map with drawing/import.
2. Save farm and field boundaries.
3. Add intervention markers/polygons.
4. Generate task/evidence checklist from templates.
5. Export JobDone work package.
6. Add basic layer overlays.
7. Add simple suitability suggestions.
8. Add grant/funding matching.

## Non-goals for MVP

- full QGIS replacement
- complex hydrological modelling
- fully automated grant advice
- exact payment calculations
- machine learning recommendations
- native mobile app
- contractor marketplace
