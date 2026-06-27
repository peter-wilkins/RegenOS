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

## First query

The first local query is intervention-first:

```bash
python3 scripts/query_grants.py check-dam --facts '{"watercourse":{"width_m":1.8}}'
```

This should return candidate funding options, rule states, and evidence prompts.
It is deliberately small: prove the linked records are useful before adding a
database or scraper.

To generate a draft JobDone work package from a selected option:

```bash
python3 scripts/generate_work_package.py \
  --project-id dewlish-water-walk \
  --intervention-id check-dam-001 \
  --template check-dam \
  --funding-option uk-england.capital-grants-2026/rp32-small-leaky-woody-dams
```
