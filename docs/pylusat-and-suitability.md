# PyLUSAT and suitability analysis

PyLUSAT is a useful reference point because it points toward the spatial problem RegenOS needs to solve:

> Given a set of map layers and criteria, where is the best place to do a particular thing?

For RegenOS, the questions might be:

- Where should ponds go?
- Where should leaky dams go?
- Where should tree belts go?
- Where should wetland restoration be prioritised?
- Where should riparian fencing be installed?
- Where would agroforestry be least disruptive and most beneficial?

## Suitability engine inputs

Potential layers:

- field boundaries
- ownership/tenancy boundaries
- LiDAR elevation
- slope
- aspect
- flow accumulation
- stream/ditch network
- soil type
- drainage class
- rainfall
- flood risk
- existing woodland
- protected habitats
- archaeology constraints
- public rights of way
- roads/access tracks
- farm infrastructure
- satellite/drone imagery

## Traditional scoring

A simple suitability model might assign scores:

- close to ditch: positive for check dam
- steep enough for flow: positive for check dam
- protected habitat: exclusion
- close to access track: positive for delivery
- productive central field area: negative
- wet unproductive corner: positive

This can create heat maps and ranked candidate sites.

## Better long-term model

Fixed expert weights are a starting point, not the end.

Over time, RegenOS could learn from completed projects:

- which ponds held water
- which trees survived
- which dams failed
- which projects were approved
- which evidence packs passed inspection
- which farmers were satisfied

That feedback could improve recommendations.

## Suitability is not approval

A good suitability score does not mean the work is legal, permitted, fundable, or ecologically appropriate.

RegenOS should separate:

1. physical suitability
2. ecological suitability
3. funding eligibility
4. legal/consent constraints
5. practical deliverability

## Possible implementation path

1. Start with simple rule-based scoring.
2. Support GeoJSON boundaries and common raster/vector layers.
3. Generate candidate intervention sites.
4. Let humans edit/approve suggestions.
5. Feed approved projects into task/evidence workflows.
6. Later add optimisation and learning.
