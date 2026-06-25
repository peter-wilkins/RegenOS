# Architecture discussion

This is deliberately not a final architecture.

The main question is where RegenOS stops and where JobDone starts.

## Candidate architecture layers

```text
User interfaces
  - map UI
  - adviser/project UI
  - field task UI via JobDone
  - evidence/claim UI

Application layer
  - project planner
  - intervention template engine
  - funding eligibility engine
  - task/evidence generator
  - claim/evidence pack builder

Domain model
  - land parcels
  - spatial layers
  - interventions
  - funding programmes/options
  - tasks
  - evidence
  - people/organisations
  - claims
  - inspections

Integration layer
  - JobDone
  - GIS data sources
  - government grant datasets/guidance
  - contractor systems
  - storage/photo systems
  - future mobile apps

Data layer
  - relational data
  - geospatial data
  - object storage for photos/docs
  - search/indexing
```

## Big architecture decision

### Option A: RegenOS owns tasks

RegenOS has its own full task model. JobDone is one execution UI/integration.

Pros:

- RegenOS remains independent
- restoration-specific logic is centralised
- easier to support multiple task systems later

Cons:

- duplicates JobDone
- more software to build
- possible drift between systems

### Option B: JobDone owns tasks

RegenOS generates restoration projects and exports them to JobDone. JobDone owns task execution and evidence capture.

Pros:

- faster MVP
- uses existing JobDone work
- clearer product separation

Cons:

- RegenOS depends on JobDone capabilities
- restoration evidence may need fields JobDone does not yet support
- harder to make RegenOS standalone later

### Option C: Shared task/evidence schema

Define a neutral work package schema. RegenOS and JobDone both consume/produce it.

Pros:

- best long-term architecture
- keeps integration clean
- could become an open standard for restoration work packages

Cons:

- requires more discipline early
- schema design can become a rabbit hole

## Current bias

Start with Option C, implemented pragmatically.

Define a simple YAML/JSON work package format. RegenOS generates it. JobDone imports/executes it. Do not overbuild the API until the field workflow is proven.

## Open technical questions

- Should the canonical data model be event-sourced?
- Should spatial data live in PostGIS from the start?
- Should intervention templates be plain YAML, database records, or code?
- Should funding rules be declarative data, executable code, or both?
- Should evidence be content-addressed and immutable?
- How much offline support is needed for field work?
- How much of the system should be local-first?
- Should this be Clojure-first, Python-first, or split by concern?

## Likely first architecture

A boring first architecture may be best:

- Postgres/PostGIS for core data
- object storage for photos/documents
- YAML templates in the repo
- Python for geospatial experiments
- existing JobDone code for tasks
- simple export/import format before live API integration

Do the simple thing first, but keep the seams clean.
