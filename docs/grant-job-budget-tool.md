# Grant job budget tool

The budget tool should help a landowner judge whether a possible grant-funded
job is economically viable.

The first version should be useful even when the numbers are rough.

## Product question

For each candidate grant job:

> If we did this here, would the grant roughly cover the work, and what are the
> biggest unknowns?

## Core records

### Grant job budget

Fields:

- `id`
- `project_id`
- `site_id`
- `intervention_id`
- `funding_option_id`
- `quantity`
- `grant_income_estimate`
- `cash_cost_estimate`
- `internal_cost_estimate`
- `margin_estimate`
- `confidence`
- `assumptions`
- `unknowns`
- `landowner_judgement`

### Resource inventory

Things the farm already has.

Fields:

- `machinery`
- `people`
- `materials`
- `access_routes`
- `storage`
- `constraints`

Examples:

- small digger
- tractor and trailer
- chainsaw-certified person
- woodland needing thinning
- pile of stone
- wet access track

### Cost line

A single assumption in the budget.

Fields:

- `kind`: labour, machinery, material, contractor, consent, maintenance, other
- `description`
- `quantity`
- `unit`
- `unit_cost`
- `cash_or_internal`
- `confidence`
- `source`

## Useful first calculation

```text
grant income
- cash costs
- internal labour and machinery cost
= rough margin
```

The margin is not accounting truth. It is a decision aid.

## Confidence

Each budget should show confidence:

- `low`: mostly guessed
- `medium`: based on local rates or previous similar jobs
- `high`: quoted, measured, or already done before

The tool should make uncertainty visible:

- "wood is free if woodland clearing happens first"
- "machine access unknown until field walk"
- "consent cost unknown"
- "contractor quote needed"

## Learning loop

After a job is completed, actual costs should update future estimates:

- actual hours
- actual machine time
- actual bought materials
- actual grant claim
- delays or hidden costs

This turns early guesswork into local cost knowledge.

## JobDone role

JobDone is the right place for the user-facing tool because it already knows:

- tasks
- teams
- sites
- observations
- photos
- evidence
- completion state

RegenOS should provide:

- grant option data
- intervention templates
- default cost assumptions
- evidence requirements

JobDone should let the landowner edit:

- what the farm owns
- what materials are nearby
- expected hours
- contractor quotes
- whether the job is worth doing

## MVP behaviour

For a Water Walk candidate pin:

1. Choose likely intervention.
2. Choose possible grant option.
3. Estimate quantity.
4. Ask what resources are already available.
5. Add rough labour/machinery/material lines.
6. Show:
   - likely grant income
   - likely cash cost
   - internal cost
   - rough margin
   - biggest unknowns
   - confidence
7. Let the landowner mark:
   - worth exploring
   - needs quote/adviser
   - not worth it

## What not to build first

- full farm accounting
- tax treatment
- depreciation model
- contractor marketplace
- automatic quote sourcing
- complex optimisation

Only add that if field use proves it changes decisions.
