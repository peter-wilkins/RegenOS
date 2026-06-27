# JobDone integration

JobDone may be the most important near-term integration point.

The insight is that grant evidence requirements are really task requirements.

## Example

A grant or funding agreement might require:

- before photos
- map of works
- contractor invoice
- GPS location
- after photos
- dimensions of installed feature
- maintenance inspection after 12 months

In RegenOS/JobDone terms, those become structured tasks and evidence fields.

## Proposed flow

```text
Water Walk / field observation
        ↓
Funding rule / adviser plan
        ↓
Intervention template
        ↓
Project work package
        ↓
JobDone task list
        ↓
Field completion + evidence capture
        ↓
Evidence pack
        ↓
Claim / report / inspection file
        ↓
Payment and variance review
        ↓
Maintenance / durability trail
```

## Task fields

A RegenOS-generated JobDone task probably needs:

- task id
- project id
- intervention id
- title
- description
- sequence/dependencies
- assignee
- location
- required tools/materials
- health and safety notes
- evidence requirements
- completion criteria
- inspection/approval status
- lifecycle phase
- gate status
- source grant requirement

## Evidence fields

Evidence should be first-class data, not random attachments.

Possible evidence types:

- photo
- video
- GPS point
- GPS track
- measurement
- sketch
- invoice
- delivery note
- contractor statement
- inspection note
- maintenance record
- sensor reading
- drone image

## Grant lifecycle tasks

Grant work packages should include submission and gate tasks, not only fieldwork
tasks.

Suggested phases:

- `explore`
- `pre_application`
- `application`
- `agreement`
- `delivery`
- `claim`
- `payment_review`
- `maintenance`

Important generated tasks:

- check land parcels and maps in Rural Payments
- confirm management control
- check existing agreements and double-funding risk
- collect required adviser support
- collect consents or permissions
- prepare before-work photos
- prepare map/sketch
- submit application
- record agreement offer and start date
- do not start work until work is allowed
- collect during/after photos
- keep invoices, receipts, and timesheets
- assemble claim pack
- submit claim
- record actual grant payment and costs
- explain estimate-vs-actual variance
- schedule maintenance/durability checks

## Field prompts

JobDone could guide the person doing the work.

Example:

> Check dam 3 complete.

System prompts:

1. Take upstream photo.
2. Take downstream photo.
3. Confirm GPS point.
4. Measure dam height.
5. Measure spillway/overflow width.
6. Add notes about materials used.
7. Mark task complete.

## Why this matters

The evidence is captured while the person is standing in the field, not reconstructed months later from WhatsApp messages, memory, and a heap of receipts.

## Integration style

Keep RegenOS and JobDone loosely coupled.

RegenOS should produce a work package. JobDone should execute it.

That suggests a simple interchange format first:

- JSON or YAML export
- stable task schema
- stable evidence schema
- later API integration

## Open question

Does JobDone own the task model, with RegenOS as a generator?

Or does RegenOS own restoration-domain tasks, with JobDone as a general execution UI?

This is probably the most important architecture decision.
