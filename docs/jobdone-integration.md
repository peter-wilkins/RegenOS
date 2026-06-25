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
