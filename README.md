# RegenOS

**RegenOS** is an open project for planning, funding, delivering, and proving land restoration work.

The basic idea is simple: regenerative land work is not just a grant application problem. It is a full delivery problem.

Farmers, landowners, advisers, contractors, volunteers, and funders need a system that can answer:

1. What could be done on this land?
2. What would it cost?
3. What funding might pay for it?
4. What tasks need doing?
5. What evidence must be captured?
6. Who will do the work?
7. Can the final claim or compliance pack be assembled automatically?

## Current focus

The first focus is practical water and habitat restoration:

- ponds
- leaky dams / check dams
- wetland restoration
- tree planting
- agroforestry
- hedgerow restoration
- riparian fencing
- soil and infiltration improvements

## Key idea

Grant requirements can be treated as structured work.

If a grant requires before photos, GPS points, invoices, measurements, maps, after photos, inspection notes, and maintenance checks, those are not vague paperwork obligations. They are tasks.

That makes this a natural integration point for **JobDone**: JobDone can become the execution, evidence, and audit layer for restoration projects.

## Repository structure

- [`docs/vision.md`](docs/vision.md) — what this project is trying to become.
- [`docs/mvp.md`](docs/mvp.md) — first useful version.
- [`docs/jobdone-integration.md`](docs/jobdone-integration.md) — how grant evidence becomes field tasks.
- [`docs/jobdone-water-walk-page.md`](docs/jobdone-water-walk-page.md) — first JobDone page for water-walk pins and evidence capture.
- [`docs/grant-model.md`](docs/grant-model.md) — country-independent grant/funding model.
- [`docs/grants-knowledge-graph.md`](docs/grants-knowledge-graph.md) — first linked-record model for grant options, eligibility, evidence, and JobDone tasks.
- [`docs/water-walk-grant-field-guide.md`](docs/water-walk-grant-field-guide.md) — what to look for in the field when matching locations to grant jobs.
- [`docs/grant-job-budget-tool.md`](docs/grant-job-budget-tool.md) — first budget model for estimating whether a grant job is economically worth doing.
- [`docs/intervention-templates.md`](docs/intervention-templates.md) — reusable templates for real-world work.
- [`docs/pylusat-and-suitability.md`](docs/pylusat-and-suitability.md) — notes on land suitability analysis.
- [`docs/architecture-discussion.md`](docs/architecture-discussion.md) — provisional architecture questions, not a final design.
- [`docs/open-questions.md`](docs/open-questions.md) — questions still unresolved.
- [`data/`](data/) — early schema/template examples.
- [`examples/`](examples/) — example restoration projects.

## Design principle

Do not hard-code one country, one grant scheme, or one government.

Model the durable things:

- land parcels
- spatial layers
- interventions
- eligibility rules
- evidence requirements
- tasks
- people and organisations
- claims
- inspections
- long-term monitoring

Then plug in country-specific schemes as data.

## Status

Very early. This is currently a thinking and design repository, not production software.
