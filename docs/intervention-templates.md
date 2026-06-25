# Intervention templates

An intervention template describes a type of real-world restoration work.

Templates should be reusable across countries and funding schemes.

A pond is still a pond whether it is funded by a government grant, a water company, a charity, or a private landowner.

## Template purpose

A template should capture:

- what the intervention is
- when it is suitable
- how it is usually delivered
- what materials/equipment are needed
- what tasks are usually required
- what evidence is usually needed
- common mistakes
- maintenance obligations

## Candidate intervention types

- pond
- leaky dam / check dam
- scrape
- wetland restoration
- floodplain reconnection
- hedge planting
- hedge laying
- tree planting
- agroforestry strip
- riparian fencing
- buffer strip
- beetle bank
- swale
- sediment trap
- livestock crossing

## Generic template structure

```yaml
id: pond
name: Pond
description: Create or restore a pond for water retention and habitat.
suitable_when:
  - wet corner
  - seasonal flow
  - low agricultural value area
avoid_when:
  - protected habitat without consent
  - high risk of damaging archaeology
  - unsafe embankment requirement
typical_tasks:
  - survey site
  - take before photos
  - mark out pond
  - check utilities/services
  - confirm permissions
  - excavate pond
  - shape banks
  - manage spoil
  - take after photos
  - schedule inspection
required_evidence:
  - before_photo
  - gps_location
  - after_photo
  - invoice_or_labour_record
  - dimensions
maintenance:
  - inspect after heavy rain
  - check erosion
  - manage invasive plants
```

## Separation from grants

Templates should not contain scheme-specific payment rates.

Instead:

- intervention template says what work is involved
- funding option says what is eligible and what evidence is required
- project combines them
- JobDone executes them

## Why this matters

This avoids rebuilding the same task logic for every country and every grant scheme.
