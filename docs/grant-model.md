# Grant and funding model

RegenOS should not be built around one current scheme.

The same core model should support:

- government grants
- private nature markets
- water company catchment schemes
- biodiversity net gain
- carbon projects
- charity-funded restoration
- local authority flood schemes
- blended funding

## Core entities

### Funding programme

A programme is a broad funding source.

Examples:

- England environmental land management scheme
- woodland creation programme
- water company catchment fund
- private biodiversity fund

Fields:

- id
- name
- country/region
- funder
- status
- start/end dates
- official guidance URL
- application route
- claim route

### Funding option

An option is a specific fundable activity or item.

Examples:

- create pond
- plant hedge
- install fencing
- plant woodland
- restore wetland
- create buffer strip

Fields:

- id
- programme id
- name
- description
- intervention type
- payment type
- payment rate
- unit
- eligibility rules
- evidence requirements
- maintenance obligations
- compatibility rules

### Eligibility rule

Rules should be data, not hard-coded logic where possible.

Possible rule types:

- country/region
- land type
- soil type
- slope
- distance to watercourse
- protected area exclusion
- existing agreement exclusion
- minimum/maximum area
- ownership/tenancy requirement
- permission/consent requirement

### Evidence requirement

Evidence requirements are the bridge to JobDone.

Fields:

- id
- funding option id
- evidence type
- when required
- task phase
- required metadata
- accepted formats
- who must provide it

### Claim

A claim is a submission against completed work.

Fields:

- id
- project id
- funding option ids
- claim status
- evidence bundle
- amount claimed
- submitted date
- approval status
- audit notes

## Important design principle

Eligibility and evidence rules should be explainable.

A user should be able to see:

> This pond appears eligible because it is in the right region, outside excluded habitat, meets the size criteria, and has the required before photos and GPS evidence.

Or:

> This tree planting proposal is blocked because it overlaps an excluded feature or needs consent.

## Caution

RegenOS should not imply that it can guarantee grant approval.

It should help prepare better applications, better evidence, and better delivery records.
