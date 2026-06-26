# JobDone Water Walk Page

## Decision

The field capture MVP should live in JobDone.

RegenOS can generate the planning data: candidate places, why they are
interesting, and what evidence to collect. JobDone already has the HTTPS,
offline-first, phone, task, and evidence capture shape.

## Page shape

Add a JobDone page for a water walk.

The page should show:

- a map
- location pins for the most interesting candidate places
- a ranked list below the map
- one-tap evidence capture for the selected pin
- offline-first local storage

Do not draw all field boundaries in the first JobDone version. The KML field
polygons are useful source data, but they are noisy on a phone map.

## Candidate pin record

Start with a small JavaScript/JSON record:

```json
{
  "id": "dewlish-higher-kitehill-001",
  "projectId": "dewlish-water-walk",
  "title": "Higher Kitehill",
  "latitude": 50.0,
  "longitude": -2.0,
  "priority": "high",
  "score": 12,
  "whyInteresting": [
    "High runoff risk",
    "Steep slope",
    "Very high erosion risk"
  ],
  "lookFor": [
    "runoff lines",
    "erosion",
    "wet corners",
    "possible interception point"
  ],
  "evidencePrompt": "Take photos of runoff paths, wet ground, ditches, slope direction, and any existing water control features."
}
```

## Route planning

The first route planning can be simple:

1. show all high/medium pins
2. let Peter toggle pins on/off
3. sort selected pins by nearest-next from current location
4. show the ordered list as the walking route

This is good enough for the first farm walk. Do not add complex routing until
there is proof that nearest-next is not good enough.

## Capture flow

When Peter opens a pin:

1. show why it was selected
2. show what to look for
3. offer `Add observation`
4. capture GPS, note, and photos
5. store locally if offline
6. attach the observation to the JobDone task/evidence model

## Boundary

RegenOS owns:

- candidate generation
- scoring rules
- source evidence references
- intervention planning

JobDone owns:

- phone UI
- offline capture
- tasks
- photos/notes/GPS evidence
- later evidence packs

## First JobDone handoff

Build a new page:

```text
Water Walk
```

Use generated candidate pins rather than field polygons. The first fixture can
be hard-coded from the current Dewlish candidates, then replaced by an import
from RegenOS JSON once the UI is useful.
