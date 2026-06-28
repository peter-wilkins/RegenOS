# Grants knowledge graph MVP

The grants knowledge graph should start as linked records in files, not a graph
database.

The first proof is simple:

> Given a site, a proposed intervention, and a funding source, can RegenOS explain
> what may be fundable, what evidence is needed, and what field tasks JobDone
> should create next?

## Why a graph

Grant guidance is not one flat table. It links:

- funding programmes
- funding options
- intervention templates
- eligibility rules
- evidence requirements
- maintenance obligations
- site facts
- work packages
- JobDone tasks
- evidence captures
- claims
- lifecycle gates
- submission tasks
- public examples and lessons

The useful graph is the set of links between those things.

## MVP records

### Programme

A broad source of funding.

Example: `uk-england.capital-grants-2026`.

Fields:

- `id`
- `name`
- `jurisdiction`
- `funder`
- `status`
- `source_urls`
- `application_notes`
- `options`

### Funding option

A specific fundable item or activity.

Example: `uk-england.capital-grants-2026/rp32-small-leaky-woody-dams`.

Fields:

- `id`
- `programme_id`
- `name`
- `intervention_templates`
- `payment`
- `eligibility_rules`
- `evidence_requirements`
- `maintenance_obligations`
- `compatibility`
- `source_urls`
- `confidence`

### Intervention template

Existing RegenOS templates such as `pond`, `check-dam`, and `tree-planting`.

The template describes the work. The funding option describes what the funder
will pay for and what proof it wants.

### Site fact

A fact about a farm, field, ditch, watercourse, soil, ownership, or evidence
capture.

Examples:

- `site.country = England`
- `watercourse.width_m = 1.8`
- `feature.type = ephemeral_runoff_pathway`
- `management_control.confirmed = true`
- `before_photos.present = true`

Site facts can come from:

- user answers
- GIS layers
- field observations
- uploaded documents
- JobDone evidence
- adviser review

### Eligibility rule

A rule that can be evaluated against site facts, or parked as a human/adviser
question.

Rule states:

- `pass`
- `fail`
- `unknown`
- `needs_human`

Unknown is not failure. Unknown means "capture more evidence or ask someone".

### Evidence requirement

The bridge to JobDone.

Evidence requirements become tasks or prompts, such as:

- take before photos
- record GPS point
- upload consent
- keep invoice
- take after photos
- record dimensions
- schedule inspection

### Lifecycle gate

A lifecycle gate says whether the grant job is allowed to move to the next
stage.

Examples:

- work cannot start before the agreement start date
- application cannot be submitted until land parcels and maps are checked
- claim cannot be submitted until work is finished and invoices or charges exist
- maintenance remains active through the durability period

Lifecycle gates should become visible JobDone tasks and warnings.

### Public example

A public example is a completed or in-progress real-world project, case study,
photo set, video, location, monitoring note, or failure report.

Examples are deliberately separate from funding options:

- a funding option says what may be paid for
- an example says what someone actually did and what can be learned

Useful fields:

- `id`
- `title`
- `location`
- `source_urls`
- `media_types`
- `related_intervention_templates`
- `likely_relevant_options`
- `learnings`

Examples should include failures and maintenance lessons where possible. A dam
that washed out, a pond that polluted, a tree planting that failed because of
browsing, or a grassland seed mix that failed because fertility stayed too high
is valuable knowledge.

The first curated file is:

- `data/grants/uk-england/public-examples.yaml`

### Lifecycle task guide

Generated JobDone lifecycle tasks should link to short practical guidance. The
current guide is:

- [`docs/grant-lifecycle-task-guide.md`](grant-lifecycle-task-guide.md)

Keep this guidance generic and reusable. Do not duplicate long how-to text in
every funding option.

## First useful queries

### 1. What might fund this intervention?

Input:

- site facts
- proposed intervention template

Output:

- matching funding options
- pass/fail/unknown eligibility explanation
- missing facts
- caution notes

### 2. What evidence should I capture next?

Input:

- funding option
- intervention template
- current evidence

Output:

- next JobDone tasks
- phase: before, delivery, claim, maintenance
- required metadata

### 3. What can go in the claim pack?

Input:

- work package
- completed JobDone tasks
- evidence captures

Output:

- evidence index
- missing items
- claim-ready status

### 4. What phase is this job in?

Input:

- grant job lifecycle state
- submitted evidence
- agreement dates
- completed tasks

Output:

- current gate
- blocked/unblocked status
- next submission tasks
- warning if work is being planned too early

## Source handling

Grant records should include source URLs and dates because rules change.

Early records can be approximate, but must say so using:

- `status: draft`
- `confidence: low|medium|high`
- `last_checked`
- `source_urls`

Do not imply grant approval is guaranteed.

## Storage choice

Start with YAML in git.

This is enough to:

- review changes
- diff grant updates
- test queries
- let agents add records
- avoid database work before the model is proven

A database can come later if we need multi-user editing, fast search, or private
site data at scale.

## First implementation slice

1. Hand-curate a tiny Capital Grants 2026 seed file.
2. Link three options to existing templates:
   - small leaky woody dams -> `check-dam`
   - large leaky woody dams -> `check-dam`
   - create or restore ponds -> `pond`
3. Write a small query script:
   - input: intervention template plus known site facts
   - output: candidate funding options and missing evidence
4. Generate a draft JobDone work package from the chosen option.

This proves the graph shape without building a universal grant scraper.

## Current scripts

Find candidate options:

```bash
python3 scripts/query_grants.py check-dam --facts '{"watercourse":{"width_m":1.8}}'
```

Generate a draft JobDone work package:

```bash
python3 scripts/generate_work_package.py \
  --project-id dewlish-water-walk \
  --intervention-id check-dam-001 \
  --template check-dam \
  --funding-option uk-england.capital-grants-2026/rp32-small-leaky-woody-dams
```

The output is a draft. It should be treated as a planning and evidence prompt,
not as confirmation that a grant application will succeed.

Related lifecycle model:

- [`docs/grant-lifecycle.md`](grant-lifecycle.md)
- [`docs/grant-lifecycle-task-guide.md`](grant-lifecycle-task-guide.md)
