# Grant data

This folder is for structured funding scheme data.

Do not assume all funding is government grant funding.

A funding source might be:

- government scheme
- water company catchment fund
- private biodiversity buyer
- charity
- local authority flood programme
- carbon/nature market

## Proposed subfolders

- `uk-england/`
- `eu/`
- `us/`
- `australia/`
- `private/`

## Suggested file shape

```yaml
id: example-programme
name: Example Programme
jurisdiction: example-country
funder: Example Funder
status: draft
url: https://example.com
options:
  - id: pond-creation
    intervention_type: pond
    payment_type: per_item
    payment_rate: null
    unit: pond
    eligibility_rules: []
    evidence_requirements: []
    maintenance_obligations: []
```

Keep early files approximate, but mark their status clearly.
