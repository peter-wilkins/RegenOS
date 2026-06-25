# Evidence types

Evidence is central to RegenOS.

It should be captured at the time work is done, not reconstructed later.

## Candidate evidence types

- photo
- video
- GPS point
- GPS track
- mapped polygon
- measurement
- invoice
- delivery note
- labour record
- contractor statement
- inspection note
- maintenance record
- drone image
- sensor reading

## Evidence metadata

Useful fields:

```yaml
id: evidence-id
type: photo
project_id: example-project
intervention_id: pond-1
task_id: task-1
captured_by: person-id
captured_at: 2026-06-25T12:00:00Z
location:
  lat: null
  lon: null
file: null
notes: null
used_in_claims: []
```

## Principle

If evidence is used in a claim or inspection pack, it should probably become immutable or at least versioned.
